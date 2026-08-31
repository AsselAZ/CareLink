import Link from "next/link";

export default function SeniorStartPage() {
  return (
    <main className="min-h-screen bg-stone-50 px-6 py-12">
      <div className="mx-auto max-w-2xl">
        {/* Link zurück zur Landingpage */}
        <Link
          href="/"
          className="font-semibold text-slate-700"
        >
          Zurück zur Startseite
        </Link>

        {/* Auswahl für neue oder bereits registrierte Senior-Nutzer */}
        <section className="mt-10 rounded-3xl border border-stone-200 bg-white p-8">
          <h1 className="text-4xl font-bold text-slate-950">
            Wie möchten Sie fortfahren?
          </h1>

          <p className="mt-4 text-lg text-slate-600">
            Erstellen Sie ein neues Konto oder melden Sie sich mit Ihrem
            bestehenden Konto an.
          </p>

          {/* Führt später zur dreistufigen Senior-Registrierung */}
          <Link
            href="/register/senior"
            className="mt-8 block rounded-2xl bg-amber-700 px-6 py-5 text-center text-xl font-bold text-white"
          >
            Neues Konto erstellen
          </Link>

          {/* Führt zum bereits funktionierenden Login */}
          <Link
            href="/login"
            className="mt-4 block rounded-2xl border-2 border-slate-800 px-6 py-5 text-center text-xl font-bold"
          >
            Ich habe bereits ein Konto
          </Link>
        </section>
      </div>
    </main>
  );
}