// src/AppRouter.tsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppLayout from './App';
import QueryConsole from './pages/QueryConsole';
import BanditDashboard from './pages/BanditDashboard';
import PromptViewer from './pages/PromptViewer';
import ExperienceLog from './pages/ExperienceLog';
import AdminPanel from './pages/AdminPanel';

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          {/* Home page - main console as default */}
          <Route index element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2 space-y-6">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8 hover:shadow-xl transition-shadow duration-300">
                  <QueryConsole />
                </div>
              </section>

              <aside className="space-y-6">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <PromptViewer />
                </div>
              </aside>
            </div>
          } />

          {/* Bandit page */}
          <Route path="bandit" element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2 space-y-6">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8 hover:shadow-xl transition-shadow duration-300">
                  <QueryConsole />
                </div>
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8 hover:shadow-xl transition-shadow duration-300">
                  <ExperienceLog />
                </div>
              </section>

              <aside className="space-y-6">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <PromptViewer />
                </div>
              </aside>
            </div>
          } />

          {/* Prompts page */}
          <Route path="prompts" element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8 hover:shadow-xl transition-shadow duration-300">
                  <PromptViewer />
                </div>
              </section>
              <aside className="space-y-6">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <ExperienceLog />
                </div>
              </aside>
            </div>
          } />

          {/* Experiences page */}
          <Route path="experiences" element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8 hover:shadow-xl transition-shadow duration-300">
                  <ExperienceLog />
                </div>
              </section>
              <aside className="space-y-6">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <PromptViewer />
                </div>
              </aside>
            </div>
          } />

          {/* Admin page */}
          <Route path="admin" element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2 space-y-6">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8 hover:shadow-xl transition-shadow duration-300">
                  <AdminPanel />
                </div>
              </section>
              <aside className="space-y-6">
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:shadow-xl transition-shadow duration-300">
                  <PromptViewer />
                </div>
              </aside>
            </div>
          } />

        </Route>
      </Routes>
    </BrowserRouter>
  );
}