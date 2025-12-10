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
          {/* main console as default */}
          <Route index element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2 space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <QueryConsole />
                </div>
              </section>

              <aside className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <PromptViewer />
                </div>
              </aside>
            </div>
          } />

          <Route path="bandit" element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2 space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <QueryConsole />
                </div>
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <ExperienceLog />
                </div>
              </section>

              <aside className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <PromptViewer />
                </div>
              </aside>
            </div>
          } />

          <Route path="prompts" element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <PromptViewer />
                </div>
              </section>
              <aside className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <ExperienceLog />
                </div>
              </aside>
            </div>
          } />

          <Route path="experiences" element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <ExperienceLog />
                </div>
              </section>
              <aside className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <PromptViewer />
                </div>
              </aside>
            </div>
          } />

          <Route path="admin" element={
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <section className="lg:col-span-2 space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <AdminPanel />
                </div>
              </section>
              <aside className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <BanditDashboard />
                </div>
                <div className="bg-white rounded-lg shadow-sm p-6">
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
