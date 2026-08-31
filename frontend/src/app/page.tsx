import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#FAF8F4] text-slate-950">
      {/* Navigation */}
      <header className="border-b border-stone-200/80 bg-[#FAF8F4]/95">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <Link href="/" className="text-2xl font-extrabold tracking-tight">
            Care<span className="text-amber-700">Link</span>
          </Link>

          <nav className="flex items-center gap-2 sm:gap-4">
            <Link
              href="/login"
              className="rounded-xl px-4 py-3 font-semibold text-slate-800 transition hover:bg-white"
            >
              Anmelden
            </Link>

            <Link
              href="/register"
              className="rounded-xl bg-slate-950 px-5 py-3 font-semibold text-white shadow-sm transition hover:bg-slate-800 focus:outline-none focus:ring-4 focus:ring-slate-300"
            >
              Registrieren
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden">
        {/* Decorative background elements create depth without affecting usability. */}
        <div className="absolute -right-32 top-10 h-96 w-96 rounded-full bg-amber-200/40 blur-3xl" />
        <div className="absolute -left-40 bottom-0 h-80 w-80 rounded-full bg-orange-100/60 blur-3xl" />

        <div className="relative mx-auto grid max-w-7xl items-center gap-16 px-6 py-20 lg:grid-cols-2 lg:py-28">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-amber-200 bg-white px-4 py-2 font-semibold text-amber-900 shadow-sm">
              <span className="h-2.5 w-2.5 rounded-full bg-amber-600" />
              Unterstützung in Ihrer Nähe
            </div>

            <h1 className="mt-7 max-w-3xl text-5xl font-extrabold leading-[1.08] tracking-tight sm:text-6xl">
              Hilfe im Alltag,
              <span className="block text-amber-700">
                wenn sie gebraucht wird.
              </span>
            </h1>

            <p className="mt-7 max-w-2xl text-xl leading-8 text-slate-700">
              CareLink verbindet Menschen, die Unterstützung benötigen, mit
              hilfsbereiten Personen aus ihrer Nachbarschaft – einfach,
              persönlich und übersichtlich.
            </p>

            <div className="mt-10 flex flex-col gap-4 sm:flex-row">
              <Link
                href="/senior/start"
                className="rounded-2xl bg-amber-700 px-8 py-5 text-center text-xl font-bold text-white shadow-lg shadow-amber-900/10 transition hover:bg-amber-800 focus:outline-none focus:ring-4 focus:ring-amber-300"
              >
                Ich benötige Hilfe
              </Link>

              <Link
                href="/helper/start"
                className="rounded-2xl border-2 border-slate-900 bg-white px-8 py-5 text-center text-xl font-bold text-slate-950 transition hover:bg-stone-100"
              >
                Ich möchte helfen
              </Link>
            </div>

            <div className="mt-9 flex flex-wrap gap-5 text-base font-semibold text-slate-700">
              <span>✓ Große, klare Bedienung</span>
              <span>✓ Hilfe aus der Umgebung</span>
              <span>✓ Direkter Kontakt</span>
            </div>
          </div>

          {/* Product preview */}
          <div className="relative mx-auto w-full max-w-xl">
            <div className="absolute -left-8 top-16 hidden rounded-2xl border border-stone-200 bg-white p-4 shadow-lg lg:block">
              <p className="text-sm text-slate-500">Entfernung</p>
              <p className="mt-1 text-xl font-bold text-slate-950">1,4 km</p>
            </div>

            <div className="absolute -right-6 bottom-16 hidden rounded-2xl border border-stone-200 bg-white p-4 shadow-lg lg:block">
              <p className="text-sm text-slate-500">Bewertung</p>
              <p className="mt-1 text-xl font-bold text-slate-950">★ 4,8</p>
            </div>

            <div className="rounded-[2rem] border border-stone-200 bg-white p-7 shadow-2xl shadow-stone-300/40 sm:p-9">
              <div className="flex items-start justify-between gap-6">
                <div>
                  <p className="font-semibold text-amber-800">
                    Offene Aufgabe
                  </p>

                  <h2 className="mt-2 text-2xl font-bold">
                    Einkauf im Supermarkt
                  </h2>
                </div>

                <span className="rounded-full bg-amber-100 px-4 py-2 text-sm font-bold text-amber-900">
                  Einkauf
                </span>
              </div>

              <p className="mt-5 text-lg leading-7 text-slate-600">
                Unterstützung beim Wocheneinkauf. Der Supermarkt befindet sich
                in der Nähe.
              </p>

              <div className="mt-7 grid grid-cols-2 gap-4">
                <div className="rounded-2xl bg-stone-100 p-5">
                  <p className="text-sm font-medium text-slate-500">
                    Entfernung
                  </p>
                  <p className="mt-1 text-lg font-bold">1,4 km</p>
                </div>

                <div className="rounded-2xl bg-stone-100 p-5">
                  <p className="text-sm font-medium text-slate-500">
                    Zeitpunkt
                  </p>
                  <p className="mt-1 text-lg font-bold">Heute</p>
                </div>
              </div>

              <div className="mt-7 rounded-2xl border border-stone-200 p-5">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-950 text-lg font-bold text-white">
                    M
                  </div>

                  <div>
                    <p className="font-bold">Michael</p>
                    <p className="text-slate-600">
                      Helfer aus Ihrer Umgebung
                    </p>
                  </div>
                </div>
              </div>

              <button
                type="button"
                className="mt-7 w-full rounded-2xl bg-slate-950 px-6 py-5 text-lg font-bold text-white transition hover:bg-slate-800"
              >
                Aufgabe ansehen
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Trust / benefits */}
      <section className="border-y border-stone-200 bg-white">
        <div className="mx-auto grid max-w-7xl gap-8 px-6 py-16 md:grid-cols-3">
          <article>
            <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-100 text-xl">
              1
            </div>

            <h2 className="text-xl font-bold">
              Einfach verständlich
            </h2>

            <p className="mt-3 leading-7 text-slate-600">
              Große Bedienelemente und eine klare Struktur reduzieren
              unnötige Schritte.
            </p>
          </article>

          <article>
            <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-100 text-xl">
              2
            </div>

            <h2 className="text-xl font-bold">
              Persönliche Unterstützung
            </h2>

            <p className="mt-3 leading-7 text-slate-600">
              Aufgaben werden von Menschen aus der Umgebung übernommen und
              gemeinsam abgestimmt.
            </p>
          </article>

          <article>
            <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-100 text-xl">
              3
            </div>

            <h2 className="text-xl font-bold">
              Sicher begleitet
            </h2>

            <p className="mt-3 leading-7 text-slate-600">
              Nachrichten, Benachrichtigungen und Bewertungen unterstützen den
              gesamten Ablauf.
            </p>
          </article>
        </div>
      </section>

      {/* Final call to action */}
      <section className="px-6 py-20">
        <div className="mx-auto max-w-5xl overflow-hidden rounded-[2rem] bg-slate-950 px-8 py-14 text-center text-white shadow-xl sm:px-12">
          <p className="font-semibold text-amber-300">
            Gemeinsam statt allein
          </p>

          <h2 className="mx-auto mt-3 max-w-3xl text-3xl font-bold sm:text-4xl">
            Unterstützung finden oder selbst einen Unterschied machen.
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-lg leading-7 text-slate-300">
            Erstellen Sie ein Konto und werden Sie Teil einer Nachbarschaft,
            die sich gegenseitig unterstützt.
          </p>

          <Link
            href="/register"
            className="mt-8 inline-block rounded-2xl bg-amber-500 px-8 py-4 text-lg font-bold text-slate-950 transition hover:bg-amber-400"
          >
            Kostenlos starten
          </Link>
        </div>
      </section>

      <footer className="border-t border-stone-200">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-8 text-sm text-slate-600 sm:flex-row sm:items-center sm:justify-between">
          <p className="font-semibold">
            CareLink
          </p>

          <p>Gemeinsam helfen. Einfach verbunden.</p>

          <p>© 2026</p>
        </div>
      </footer>
    </main>
  );
}