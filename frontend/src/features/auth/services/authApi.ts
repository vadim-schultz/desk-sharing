import { url } from '../../deskBooking/services/deskApi';

export interface AuthTokenResponse {
  access_token: string;
  expires_in: number;
}

export async function requestToken(password: string): Promise<AuthTokenResponse> {
  const res = await fetch(url('/auth/token'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  });
  if (!res.ok) {
    let message = await res.text();
    try {
      const body = JSON.parse(message) as { detail?: string };
      if (body.detail) {
        message = body.detail;
      }
    } catch {
      /* keep raw */
    }
    throw new Error(message);
  }
  return (await res.json()) as AuthTokenResponse;
}
