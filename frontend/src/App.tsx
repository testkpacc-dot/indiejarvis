// src/App.tsx
import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';

function Nav() {
  return (
    <header className="bg-white border-b">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-md bg-teal-50 flex items-center justify-center text-teal-600 font-semibold">AP</div>
          <div>
            <h1 className="text-lg font-bold">Adaptive Prompt Console</h1>
            <div className="text-sm text-gray-500">Agentic prompt system — demo</div>
          </div>
        </div>

        <nav className="text-sm">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `px-3 py-1 rounded ${isActive ? 'bg-teal-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`
            }
            end
          >
            Console
          </NavLink>

          <NavLink
            to="/bandit"
            className={({ isActive }) =>
              `px-3 py-1 rounded ${isActive ? 'bg-teal-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`
            }
          >
            Bandit
          </NavLink>

          <NavLink
            to="/prompts"
            className={({ isActive }) =>
              `px-3 py-1 rounded ${isActive ? 'bg-teal-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`
            }
          >
            Prompts
          </NavLink>

          <NavLink
            to="/experiences"
            className={({ isActive }) =>
              `px-3 py-1 rounded ${isActive ? 'bg-teal-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`
            }
          >
            Experiences
          </NavLink>

          <NavLink
            to="/admin"
            className={({ isActive }) =>
              `px-3 py-1 rounded ${isActive ? 'bg-rose-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`
            }
          >
            Admin
          </NavLink>
        </nav>
      </div>
    </header>
  );
}

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      <Nav />
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Render the active route's component here */}
        <Outlet />
      </main>
    </div>
  );
}
