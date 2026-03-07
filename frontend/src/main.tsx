import React from "react";
import ReactDOM from "react-dom/client";
import { ThemeProvider } from "@crayonai/react-ui";
import App from "./App.tsx";
import "./index.css";
import "@crayonai/react-ui/styles/index.css";
import "../node_modules/@thesysai/genui-sdk/dist/genui-sdk.css";

import { ClerkProvider } from "@clerk/clerk-react";

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
      <ThemeProvider>
        <App />
      </ThemeProvider>
    </ClerkProvider>
  </React.StrictMode>
)
