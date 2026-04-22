import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react';

import { requestToken } from '../services/authApi';

const STORAGE_KEY = 'desk-sharing-admin-auth';
const EXPIRY_BUFFER_MS = 5_000;

interface AuthState {
  token: string | null;
  expiresAt: number | null;
}

interface AuthContextValue {
  getToken: () => string | null;
  isAuthenticated: boolean;
  authenticate: (password: string) => Promise<string>;
  clearToken: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function readStored(): AuthState {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return { token: null, expiresAt: null };
    }
    const parsed = JSON.parse(raw) as { token: string; expiresAt: number };
    if (!parsed.token || !parsed.expiresAt) {
      return { token: null, expiresAt: null };
    }
    return { token: parsed.token, expiresAt: parsed.expiresAt };
  } catch {
    return { token: null, expiresAt: null };
  }
}

function writeStored(state: AuthState) {
  if (!state.token || !state.expiresAt) {
    sessionStorage.removeItem(STORAGE_KEY);
    return;
  }
  sessionStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({ token: state.token, expiresAt: state.expiresAt }),
  );
}

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [auth, setAuth] = useState<AuthState>(() => readStored());

  const getToken = useCallback((): string | null => {
    if (
      auth.token &&
      auth.expiresAt &&
      Date.now() < auth.expiresAt - EXPIRY_BUFFER_MS
    ) {
      return auth.token;
    }
    return null;
  }, [auth]);

  const isAuthenticated =
    !!auth.token &&
    !!auth.expiresAt &&
    Date.now() < auth.expiresAt - EXPIRY_BUFFER_MS;

  const authenticate = useCallback(async (password: string): Promise<string> => {
    const { access_token, expires_in } = await requestToken(password);
    const next: AuthState = {
      token: access_token,
      expiresAt: Date.now() + expires_in * 1000,
    };
    setAuth(next);
    writeStored(next);
    return access_token;
  }, []);

  const clearToken = useCallback(() => {
    const next = { token: null, expiresAt: null };
    setAuth(next);
    writeStored(next);
  }, []);

  const value = useMemo(
    () => ({ getToken, isAuthenticated, authenticate, clearToken }),
    [getToken, isAuthenticated, authenticate, clearToken],
  );

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
};

/* eslint-disable react-refresh/only-export-components -- hook is tied to this provider */
export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return ctx;
};
