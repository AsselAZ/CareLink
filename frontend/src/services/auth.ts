// Daten, die das Login-Formular an den Auth-Service übergibt.
export type LoginData = {
  email: string;
  password: string;
};

// Antwort, die FastAPI nach erfolgreichem Login zurückgibt.
export type LoginResponse = {
  access_token: string;
  token_type: string;
};

// Sendet die Login-Daten an das FastAPI-Backend.
// promise<LoginResponse> gibt ein objekt zurück, das die LoginResponse enthält
export async function login(data: LoginData):Promise<LoginResponse>  {
  const response = await fetch("http://127.0.0.1:8000/auth/login", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify(data),
  });

  // Bei 4xx oder 5xx liefert fetch keinen eigenen Fehler.
  // Deshalb prüfen wir den HTTP-Status selbst
  if (!response.ok) {
    throw new Error("Anmeldung fehlgeschlagen.");
  }

  return response.json();
}


// Daten des aktuell eingeloggten Nutzers
export type CurrentUser = {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  role: string;
};

// Ruft die Daten des eingeloggten Nutzers über den gespeicherten JWT ab
export async function getCurrentUser(
  token: string
): Promise<CurrentUser> {
  const response = await fetch("http://127.0.0.1:8000/users/me", {
    method: "GET",

    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  // Ohne gültigen Token darf das Backend die Nutzerdaten nicht zurückgeben
  if (!response.ok) {
    throw new Error("Nutzerdaten konnten nicht geladen werden.");
  }

  return response.json();
}


export type RegisterData = {
  first_name: string;
  last_name: string;
  birth_date: string;
  email: string;
  password: string;
  role: string;
};



export async function register(data: RegisterData) {
  const response = await fetch("http://127.0.0.1:8000/users/register",{
    method: "POST",
    headers:{
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),

  });
  if (!response.ok) {
    throw new Error("Regestrierung fehlgeschlagen");
  }
  return response.json();
}
