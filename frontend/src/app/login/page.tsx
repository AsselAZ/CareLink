//the page is interactive for useState
"use client";
import { login } from "@/services/auth";
import Link from "next/link";
import { useState } from "react";

export default function LoginPage() {
  // useState stores values that can change while the user interacts with the page.
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
  event.preventDefault();

  try {
    //wait for the login function to complete and return data
    const data = await login({
      email,
      password,
    });

    console.log("Login erfolgreich:", data);
  } catch (error) {
    console.error("Login fehlgeschlagen:", error);
  }
}

  return (
    <main className="min-h-screen bg-stone-50 px-6 py-12">
      <div className="mx-auto w-full max-w-md">
        <Link
          href="/"
          className="text-2xl font-bold text-slate-900"
        >
          Care<span className="text-amber-700">Link</span>
        </Link>

        <section className="mt-10 rounded-3xl border border-stone-200 bg-white p-8 shadow-sm">
          <h1 className="text-3xl font-bold text-slate-950">
            Anmelden
          </h1>

          <p className="mt-3 text-lg text-slate-600">
            Melden Sie sich mit Ihrer E-Mail-Adresse und Ihrem Passwort an.
          </p>

          <form
            onSubmit={handleSubmit}
            className="mt-8 space-y-6"
          >
            <div>
              <label
                htmlFor="email"
                className="block text-lg font-semibold text-slate-800"
              >
                E-Mail-Adresse
              </label>

              <input
                id="email"
                type="email"
                value={email}
                //if input changes, setEmail to the new value
                onChange={(event) => setEmail(event.target.value)}
                required
                className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-4 text-lg text-slate-900 outline-none focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-lg font-semibold text-slate-800"
              >
                Passwort
              </label>

              <input
                id="password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
                className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-4 text-lg text-slate-900 outline-none focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
              />
            </div>

            <button
              type="submit"
              className="w-full rounded-xl bg-amber-700 px-6 py-4 text-lg font-bold text-white transition hover:bg-amber-800 focus:outline-none focus:ring-4 focus:ring-amber-300"
            >
              Anmelden
            </button>
          </form>

          <p className="mt-8 text-center text-base text-slate-600">
            Noch kein Konto?{" "}
            <Link
              href="/register"
              className="font-semibold text-amber-800 underline"
            >
              Jetzt registrieren
            </Link>
          </p>
        </section>
      </div>
    </main>
  );
}