"use client";

import Link from "next/link";
import { useState } from "react";

export default function SeniorRegisterPage() {
    // Bestimmt, welcher Registrierungsschritt angezeigt wird.
    const [step, setStep] = useState(1);

    // Persönliche Angaben
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");

    // Fehlermeldungen für die einzelnen Eingabefelder
    const [firstNameError, setFirstNameError] = useState("");
    const [lastNameError, setLastNameError] = useState("");
    const [emailError, setEmailError] = useState("");

    const [birthDate, setBirthDate] = useState("");
    const [birthDateError, setBirthDateError] = useState("");

    // Passwortdaten 
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    // Fehlermeldungen für die Passwortfelder
    const [passwordError, setPasswordError] = useState("");
    const [confirmPasswordError, setConfirmPasswordError] = useState("");

    // Adressdaten 
    const [street, setStreet] = useState("");
    const [houseNumber, setHouseNumber] = useState("");
    const [postalCode, setPostalCode] = useState("");
    const [city, setCity] = useState("");

    // Fehlermeldungen für die Adressfelder
    const [streetError, setStreetError] = useState("");
    const [houseNumberError, setHouseNumberError] = useState("");
    const [postalCodeError, setPostalCodeError] = useState("");
    const [cityError, setCityError] = useState("");

    function validateFirstName(value: string) {
        if (!value.trim()) {
            return "Bitte geben Sie Ihren Vornamen ein.";
        }

        // Erlaubt Buchstaben, Umlaute, Leerzeichen und Bindestriche. 
        if (!/^[A-Za-zÄÖÜäöüß\s-]+$/.test(value)) {
            return "Der Vorname darf nur Buchstaben enthalten.";
        }
        // returns an empty string if the input is valid
        return "";
    }

    function validateLastName(value: string) {
        if (!value.trim()) {
            return "Bitte geben Sie Ihren Nachnamen ein.";
        }

        // Erlaubt Buchstaben, Umlaute, Leerzeichen und Bindestriche.
        if (!/^[A-Za-zÄÖÜäöüß\s-]+$/.test(value)) {
            return "Der Nachname darf nur Buchstaben enthalten.";
        }

        return "";
    }

    function validateBirthDate(value: string) {
        if (!value.trim()) {
            return "Bitte geben Sie Ihr Geburtsdatum ein.";
        }

        return "";
    }

    function validateEmail(value: string) {
        if (!value.trim()) {
            return "Bitte geben Sie Ihre E-Mail-Adresse ein.";
        }

        // Einfache Prüfung auf ein sinnvolles E-Mail-Format.
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
            return "Bitte geben Sie eine gültige E-Mail-Adresse ein.";
        }

        return "";
    }

    function validatePassword(value: string) {
        if (!value) {
            return "Bitte geben Sie ein Passwort ein.";
        }

        if (value.length < 8) {
            return "Das Passwort muss mindestens 8 Zeichen lang sein.";
        }

        return "";
    }
    function validateConfirmPassword(value: string) {
        if (!value) {
            return "Bitte bestätigen Sie Ihr Passwort.";
        }

        if (value !== password) {
            return "Die Passwörter stimmen nicht überein.";
        }

        return "";
    }

    function validateStreet(value: string) {
        if (!value.trim()) {
            return "Bitte geben Sie Ihre Straße ein.";
        }

        return "";
    }

    function validateHouseNumber(value: string) {
        if (!value.trim()) {
            return "Bitte geben Sie Ihre Hausnummer ein.";
        }

        return "";
    }

    function validatePostalCode(value: string) {
        if (!value.trim()) {
            return "Bitte geben Sie Ihre Postleitzahl ein.";
        }

        if (!/^\d{5}$/.test(value)) {
            return "Die Postleitzahl muss aus 5 Ziffern bestehen.";
        }

        return "";
    }

    function validateCity(value: string) {
        if (!value.trim()) {
            return "Bitte geben Sie Ihre Stadt ein.";
        }

        if (!/^[A-Za-zÄÖÜäöüß\s-]+$/.test(value)) {
            return "Die Stadt darf nur Buchstaben enthalten.";
        }

        return "";
    }

    function goToNextStep() {
        // Prüft alle Felder, bevor der nächste Schritt geöffnet wird.
        const newFirstNameError = validateFirstName(firstName);
        const newLastNameError = validateLastName(lastName);
        const newEmailError = validateEmail(email);
        const newBirthDateError = validateBirthDate(birthDate);

        setFirstNameError(newFirstNameError);
        setLastNameError(newLastNameError);
        setEmailError(newEmailError);
        setBirthDateError(newBirthDateError);

        // Solange mindestens ein Fehler vorhanden ist, bleiben wir auf Schritt 1.
        if (
            newFirstNameError ||
            newLastNameError ||
            newEmailError ||
            newBirthDateError
        ) {
            return;
        }

        setStep(2);
    }

    function goToPasswordNextStep() {
        // Prüft beide Passwortfelder vor Schritt 3
        const newPasswordError = validatePassword(password);
        const newConfirmPasswordError = validateConfirmPassword(confirmPassword);

        setPasswordError(newPasswordError);
        setConfirmPasswordError(newConfirmPasswordError);

        // Bei einem Fehler bleibt der Nutzer auf Schritt 2.
        if (newPasswordError || newConfirmPasswordError) {
            return;
        }

        setStep(3);
    }

    function handleRegistration() {
        // Prüft alle Adressfelder vor dem Absenden.
        const newStreetError = validateStreet(street);
        const newHouseNumberError = validateHouseNumber(houseNumber);
        const newPostalCodeError = validatePostalCode(postalCode);
        const newCityError = validateCity(city);

        setStreetError(newStreetError);
        setHouseNumberError(newHouseNumberError);
        setPostalCodeError(newPostalCodeError);
        setCityError(newCityError);

        // Bei einem Fehler bleibt der Nutzer auf Schritt 3.
        if (
            newStreetError ||
            newHouseNumberError ||
            newPostalCodeError ||
            newCityError
        ) {
            return;
        }

        // Alle Adressdaten sind gültig.
        // Danach wird die Übersicht angezeigt.
        setStep(4);
    }

    return (
        <main className="min-h-screen bg-stone-50 px-6 py-12">
            <div className="mx-auto max-w-2xl">
                {/* Zurück zum Senior-Einstieg */}
                {/* Verlässt die Registrierung und führt zurück zur Senior-Startseite */}
                <Link
                    href="/senior/start"
                    className="inline-flex items-center gap-2 rounded-xl border-2 border-amber-700 bg-white px-5 py-3 text-base font-bold text-amber-800 transition hover:bg-amber-50 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-amber-200"
                >
                    <span aria-hidden="true">←</span>
                    Zurück zur Startseite
                </Link>

                {/* Überschrift der Registrierung */}
                <header className="mt-8">
                    <p className="font-semibold text-amber-700">
                        CareLink
                    </p>

                    <h1 className="mt-2 text-4xl font-bold text-slate-950">
                        Konto erstellen
                    </h1>

                    <p className="mt-4 text-lg leading-8 text-slate-600">
                        Wir führen Sie in drei einfachen Schritten durch die Registrierung.
                    </p>
                </header>

                {/* Fortschrittsanzeige nur während der drei Eingabeschritte */}
                {step <= 3 && (
                    <div className="mt-10">
                        <div className="flex items-center justify-between font-semibold text-slate-700">
                            <span>Schritt {step} von 3</span>
                            <span>{Math.round((step / 3) * 100)} %</span>
                        </div>

                        <div className="mt-3 h-3 overflow-hidden rounded-full bg-stone-200">
                            <div
                                className="h-full rounded-full bg-amber-700 transition-all"
                                style={{ width: `${(step / 3) * 100}%` }}
                            />
                        </div>
                    </div>
                )}

                {/* Schritt 1: persönliche Angaben */}
                {step === 1 && (
                    <section className="mt-10 rounded-3xl border border-stone-200 bg-white p-8 shadow-sm">
                        <h2 className="text-2xl font-bold text-slate-950">
                            Persönliche Angaben
                        </h2>

                        <p className="mt-3 text-lg text-slate-600">
                            Bitte geben Sie Ihre persönlichen Daten ein.
                        </p>

                        <div className="mt-8 space-y-6">
                            {/* Vorname */}
                            <div>
                                <label
                                    htmlFor="firstName"
                                    className="block text-lg font-semibold text-slate-800"
                                >
                                    Vorname
                                </label>

                                <input
                                    id="firstName"
                                    type="text"
                                    value={firstName}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setFirstName(value);

                                        // Entfernt die Fehlermeldung direkt,
                                        // sobald der eingegebene Wert wieder korrekt ist.
                                        if (firstNameError) {
                                            setFirstNameError(validateFirstName(value));
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${firstNameError
                                        ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                        : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {firstNameError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {firstNameError}
                                    </p>
                                )}
                            </div>

                            {/* Nachname */}
                            <div>
                                <label
                                    htmlFor="lastName"
                                    className="block text-lg font-semibold text-slate-800"
                                >
                                    Nachname
                                </label>

                                <input
                                    id="lastName"
                                    type="text"
                                    value={lastName}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setLastName(value);

                                        if (lastNameError) {
                                            setLastNameError(validateLastName(value));
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${lastNameError
                                        ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                        : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {lastNameError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {lastNameError}
                                    </p>
                                )}
                            </div>

                            {/* Geburtsdatum */}
                            <div>
                                <label htmlFor="birthdate" className="block text-lg font-semibold text-slate-800"

                                >
                                    Geburtsdatum
                                </label>

                                <input
                                    id="birthDate"
                                    type="date"
                                    value={birthDate}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setBirthDate(value);

                                        if (birthDateError) {
                                            setBirthDateError(validateBirthDate(value));
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${birthDateError
                                            ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                            : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {birthDateError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {birthDateError}
                                    </p>
                                )}
                            </div>
                            {/* E-Mail-Adresse */}
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
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setEmail(value);

                                        if (emailError) {
                                            setEmailError(validateEmail(value));
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${emailError
                                        ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                        : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {emailError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {emailError}
                                    </p>
                                )}
                            </div>
                        </div>

                        {/* Prüft erst alle Felder und öffnet nur bei gültigen Daten Schritt 2 */}
                        <button
                            type="button"
                            onClick={goToNextStep}
                            className="mt-8 w-full rounded-2xl bg-amber-700 px-6 py-5 text-xl font-bold text-white transition hover:bg-amber-800 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-amber-300"
                        >
                            Weiter
                        </button>
                    </section>
                )}

                {/* Schritt 2 ist noch unser Testbereich */}
                {/* Schritt 2: Passwort festlegen */}
                {step === 2 && (
                    <section className="mt-10 rounded-3xl border border-stone-200 bg-white p-8 shadow-sm">
                        <h2 className="text-2xl font-bold text-slate-950">
                            Passwort festlegen
                        </h2>

                        <p className="mt-3 text-lg text-slate-600">
                            Wählen Sie ein Passwort mit mindestens 8 Zeichen.
                        </p>

                        <div className="mt-8 space-y-6">
                            {/* Eingabefeld für das Passwort */}
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
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setPassword(value);

                                        if (passwordError) {
                                            setPasswordError(validatePassword(value));
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${passwordError
                                        ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                        : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {passwordError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {passwordError}
                                    </p>
                                )}
                            </div>

                            {/* Zweites Feld zur Kontrolle des Passworts */}
                            <div>
                                <label
                                    htmlFor="confirmPassword"
                                    className="block text-lg font-semibold text-slate-800"
                                >
                                    Passwort bestätigen
                                </label>

                                <input
                                    id="confirmPassword"
                                    type="password"
                                    value={confirmPassword}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setConfirmPassword(value);

                                        if (confirmPasswordError) {
                                            if (!value) {
                                                setConfirmPasswordError(
                                                    "Bitte bestätigen Sie Ihr Passwort."
                                                );
                                            } else if (value !== password) {
                                                setConfirmPasswordError(
                                                    "Die Passwörter stimmen nicht überein."
                                                );
                                            } else {
                                                setConfirmPasswordError("");
                                            }
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${confirmPasswordError
                                        ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                        : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {confirmPasswordError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {confirmPasswordError}
                                    </p>
                                )}
                            </div>
                        </div>

                        {/* Navigation zwischen Schritt 1 und Schritt 3 */}
                        <div className="mt-8 flex gap-4">
                            <button
                                type="button"
                                onClick={() => setStep(1)}
                                className="w-1/3 rounded-2xl border-2 border-slate-300 px-6 py-5 text-lg font-bold text-slate-800 hover:bg-stone-50"
                            >
                                Zurück
                            </button>

                            <button
                                type="button"
                                onClick={goToPasswordNextStep}
                                className="w-2/3 rounded-2xl bg-amber-700 px-6 py-5 text-xl font-bold text-white transition hover:bg-amber-800 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-amber-300"
                            >
                                Weiter
                            </button>
                        </div>
                    </section>
                )}

                {/* Schritt 3: Adresse */}
                {step === 3 && (
                    <section className="mt-10 rounded-3xl border border-stone-200 bg-white p-8 shadow-sm">
                        <h2 className="text-2xl font-bold text-slate-950">
                            Ihre Adresse
                        </h2>

                        <p className="mt-3 text-lg text-slate-600">
                            Bitte geben Sie Ihre aktuelle Adresse ein.
                        </p>

                        <div className="mt-8 space-y-6">
                            {/* Straße */}
                            <div>
                                <label
                                    htmlFor="street"
                                    className="block text-lg font-semibold text-slate-800"
                                >
                                    Straße
                                </label>

                                <input
                                    id="street"
                                    type="text"
                                    value={street}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setStreet(value);

                                        if (streetError) {
                                            setStreetError(validateStreet(value));
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${streetError
                                        ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                        : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {streetError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {streetError}
                                    </p>
                                )}
                            </div>

                            {/* Hausnummer */}
                            <div>
                                <label
                                    htmlFor="houseNumber"
                                    className="block text-lg font-semibold text-slate-800"
                                >
                                    Hausnummer
                                </label>

                                <input
                                    id="houseNumber"
                                    type="text"
                                    value={houseNumber}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setHouseNumber(value);

                                        if (houseNumberError) {
                                            setHouseNumberError(validateHouseNumber(value));
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${houseNumberError
                                        ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                        : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {houseNumberError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {houseNumberError}
                                    </p>
                                )}
                            </div>

                            {/* Postleitzahl */}
                            <div>
                                <label
                                    htmlFor="postalCode"
                                    className="block text-lg font-semibold text-slate-800"
                                >
                                    Postleitzahl
                                </label>

                                <input
                                    id="postalCode"
                                    type="text"
                                    inputMode="numeric"
                                    maxLength={5}
                                    value={postalCode}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setPostalCode(value);

                                        if (postalCodeError) {
                                            setPostalCodeError(validatePostalCode(value));
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${postalCodeError
                                        ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                        : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {postalCodeError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {postalCodeError}
                                    </p>
                                )}
                            </div>

                            {/* Stadt */}
                            <div>
                                <label
                                    htmlFor="city"
                                    className="block text-lg font-semibold text-slate-800"
                                >
                                    Stadt
                                </label>

                                <input
                                    id="city"
                                    type="text"
                                    value={city}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        setCity(value);

                                        if (cityError) {
                                            setCityError(validateCity(value));
                                        }
                                    }}
                                    className={`mt-2 w-full rounded-xl border px-4 py-4 text-lg text-slate-950 outline-none ${cityError
                                        ? "border-red-600 focus:border-red-600 focus:ring-2 focus:ring-red-200"
                                        : "border-slate-300 focus:border-amber-700 focus:ring-2 focus:ring-amber-200"
                                        }`}
                                />

                                {cityError && (
                                    <p className="mt-2 font-medium text-red-700">
                                        {cityError}
                                    </p>
                                )}
                            </div>
                        </div>

                        {/* Navigation und Abschluss der Registrierung */}
                        <div className="mt-8 flex gap-4">
                            <button
                                type="button"
                                onClick={() => setStep(2)}
                                className="w-1/3 rounded-2xl border-2 border-slate-300 px-6 py-5 text-lg font-bold text-slate-800 hover:bg-stone-50"
                            >
                                Zurück
                            </button>

                            <button
                                type="button"
                                onClick={handleRegistration}
                                className="w-2/3 rounded-2xl bg-amber-700 px-6 py-5 text-xl font-bold text-white transition hover:bg-amber-800 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-amber-300"
                            >
                                Angaben überprüfen
                            </button>
                        </div>
                    </section>
                )}

                {/* Übersicht vor dem endgültigen Absenden der Registrierung */}
                {step === 4 && (
                    <section className="mt-10 rounded-3xl border border-stone-200 bg-white p-8 shadow-sm">
                        <h2 className="text-2xl font-bold text-slate-950">
                            Ihre Angaben überprüfen
                        </h2>

                        <p className="mt-3 text-lg text-slate-600">
                            Bitte prüfen Sie Ihre Angaben noch einmal, bevor Sie Ihr Konto erstellen.
                        </p>

                        {/* Persönliche Daten */}
                        <div className="mt-8 rounded-2xl border border-stone-200 p-6">
                            <h3 className="text-xl font-bold text-slate-950">
                                Persönliche Angaben
                            </h3>

                            <div className="mt-5 space-y-4">
                                <div>
                                    <p className="text-sm font-semibold text-slate-500">
                                        Vorname
                                    </p>
                                    <p className="text-lg font-semibold text-slate-950">
                                        {firstName}
                                    </p>
                                </div>

                                <div>
                                    <p className="text-sm font-semibold text-slate-500">
                                        Nachname
                                    </p>
                                    <p className="text-lg font-semibold text-slate-950">
                                        {lastName}
                                    </p>
                                </div>

                                <div>
                                    <p className="text-sm font-semibold text-slate-500">
                                        E-Mail-Adresse
                                    </p>
                                    <p className="text-lg font-semibold text-slate-950">
                                        {email}
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Adresse */}
                        <div className="mt-6 rounded-2xl border border-stone-200 p-6">
                            <h3 className="text-xl font-bold text-slate-950">
                                Adresse
                            </h3>

                            <div className="mt-5 space-y-4">
                                <div>
                                    <p className="text-sm font-semibold text-slate-500">
                                        Straße und Hausnummer
                                    </p>
                                    <p className="text-lg font-semibold text-slate-950">
                                        {street} {houseNumber}
                                    </p>
                                </div>

                                <div>
                                    <p className="text-sm font-semibold text-slate-500">
                                        Postleitzahl und Stadt
                                    </p>
                                    <p className="text-lg font-semibold text-slate-950">
                                        {postalCode} {city}
                                    </p>
                                </div>
                            </div>
                        </div>



                        {/* Nutzer kann zurückgehen oder die Registrierung endgültig absenden */}
                        <div className="mt-8 flex gap-4">
                            <button
                                type="button"
                                onClick={() => setStep(3)}
                                className="w-1/3 rounded-2xl border-2 border-slate-300 px-6 py-5 text-lg font-bold text-slate-800 hover:bg-stone-50"
                            >
                                Zurück
                            </button>

                            <button
                                type="button"
                                onClick={() => {
                                    console.log("Registrierung wird später hier abgesendet.");
                                }}
                                className="w-2/3 rounded-2xl bg-amber-700 px-6 py-5 text-xl font-bold text-white transition hover:bg-amber-800 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-amber-300"
                            >
                                Konto erstellen
                            </button>
                        </div>
                    </section>
                )}
            </div>
        </main>
    );
}