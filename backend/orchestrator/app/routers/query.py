from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any
import asyncio

from app.services.context_builder import ContextBuilder
from app.services import selector_client, prompt_registry_client, inference_client, verifier_client, experience_client
from app.utils.http_client import AsyncHttpClient
from app.schemas.query_request import QueryRequest

router = APIRouter()


@router.post("/query")
async def query_endpoint(req: QueryRequest, request: Request):
    request_id = request.headers.get("X-Request-ID") or f"req-{int(asyncio.get_event_loop().time()*1000)}"
    ctx_builder = ContextBuilder()
    context = ctx_builder.build(req)
    context.setdefault("_meta", {})
    context["_meta"]["request_id"] = request_id

    async with AsyncHttpClient() as client:
        try:
            # 2. choose prompt
            prompt_id = await selector_client.choose(client, context)

            # 3. get prompt text
            prompt_obj = await prompt_registry_client.get_prompt(client, prompt_id)
            prompt_text = prompt_obj.get("text", "")
            context["prompt_meta"] = prompt_obj.get("metadata", {})

            # 4. inference
            llm = await inference_client.generate(client, prompt_id, prompt_text, context)
            response_text = llm.get("response_text")
            trace = llm.get("trace")

            # 5. verifier
            verifier = await verifier_client.verify(client, prompt_id, context, response_text)

            # 6. update bandit (best-effort)
            try:
                await selector_client.reward(client, prompt_id, int(verifier.get("reward", 0)), metadata=verifier.get("details", {}))
            except Exception:
                pass

            # 7. log experience (best-effort)
            experience = {
                "context": context,
                "prompt_id": prompt_id,
                "response": {"text": response_text, "trace": trace},
                "verifier_result": verifier,
                "feedback": None,
                "timestamp": asyncio.get_event_loop().time(),
            }
            try:
                await experience_client.log(client, experience)
            except Exception:
                pass

            # 8. return
            return {"ok": True, "data": {"response_text": response_text, "prompt_id": prompt_id, "verifier_result": verifier}}

        except Exception as exc:
            # fallback
            fallback = f"Temporary failure — could not compute answer. Echo: {req.text}"
            try:
                await experience_client.log(client, {
                    "context": context,
                    "prompt_id": None,
                    "response": {"text": fallback, "trace": None},
                    "verifier_result": {"reward": 0, "tags": ["fallback"], "details": {"error": str(exc)}},
                    "feedback": None,
                    "timestamp": asyncio.get_event_loop().time(),
                })
            except Exception:
                pass
            raise HTTPException(status_code=502, detail={"message": str(exc), "fallback": fallback})
