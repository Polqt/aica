'use client';

import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from 'react';
import { User } from '../types/api';
import { toast } from 'sonner';
import { apiClient } from '../services/api-client';

interface AuthContextType {
  user: User | null;
  setUser: (user: User | null) => void;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshAuth: () => Promise<void>;
  fetchUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = user !== null;

  useEffect(() => {
    // Reuse fetchUser to avoid duplicating logic
    fetchUser().finally(() => setIsLoading(false));
  }, []);

  const fetchUser = async (): Promise<void> => {
    try {
      const currentUser = await apiClient.auth.getCurrentUser();
      setUser(currentUser);
    } catch {
      setUser(null);
      throw new Error('Failed to fetch user data');
    }
  };

  const login = async (email: string, password: string): Promise<void> => {
    try {
      const auth = await apiClient.auth.login({ email, password });
      // Persist access token for subsequent Authorization header (dev-friendly)
      try {
        if (auth?.access_token) {
          localStorage.setItem('access_token', auth.access_token);
        }
      } catch {}
      await fetchUser();
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Login failed';
      throw new Error(message);
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await apiClient.auth.logout();
    } catch {
      toast.error(
        'Logout request failed, but you have been logged out locally',
      );
    } finally {
      setUser(null);
    }
  };

  const refreshAuth = async (): Promise<void> => {
    try {
      await apiClient.auth.refresh();
      await fetchUser();
    } catch {
      setUser(null);
      throw new Error('Session refresh failed, please log in again.');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        isLoading,
        isAuthenticated,
        login,
        logout,
        refreshAuth,
        fetchUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context == undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
