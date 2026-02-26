import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

import { ClerkProvider, useAuth } from "@clerk/clerk-react";
import { ConvexReactClient } from "convex/react";
import { ConvexProviderWithClerk } from "convex/react-clerk";

function cleanEnvValue(raw: unknown): string {
  return String(raw ?? "")
    .trim()
    .replace(/^['"`]+|['"`]+$/g, "")
    .replace(/\s+/g, "")
    .replace(/^n(?=https?:\/\/)/i, "");
}

// Validar env vars
const PUBLISHABLE_KEY = cleanEnvValue(import.meta.env.VITE_CLERK_PUBLISHABLE_KEY);
if (!PUBLISHABLE_KEY) {
  throw new Error("Missing VITE_CLERK_PUBLISHABLE_KEY in .env.local");
}

const CONVEX_URL = cleanEnvValue(import.meta.env.VITE_CONVEX_URL);
if (!CONVEX_URL) {
  throw new Error("Missing VITE_CONVEX_URL in .env.local");
}

if (!/^https?:\/\//i.test(CONVEX_URL)) {
  throw new Error(`Invalid VITE_CONVEX_URL: "${CONVEX_URL}"`);
}

// Criar cliente Convex
const convex = new ConvexReactClient(CONVEX_URL);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ClerkProvider
      publishableKey={PUBLISHABLE_KEY}
      afterSignOutUrl="/login"
      signInForceRedirectUrl="/dashboard"
      signInFallbackRedirectUrl="/dashboard"
      signUpForceRedirectUrl="/dashboard"
      signUpFallbackRedirectUrl="/dashboard"
    >
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        <App />
      </ConvexProviderWithClerk>
    </ClerkProvider>
  </React.StrictMode>
)
