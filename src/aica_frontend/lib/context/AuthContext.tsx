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
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = user !== null;

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const currentUser = await apiClient.auth.getCurrentUser();
      setUser(currentUser);
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string): Promise<void> => {
    try {
      await apiClient.auth.login({ email, password });

      const currentUser = await apiClient.auth.getCurrentUser();
      setUser(currentUser);
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
      const currentUser = await apiClient.auth.getCurrentUser();
      setUser(currentUser);
    } catch {
      setUser(null);
      throw new Error('Session refresh failed, please log in again.');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated,
        login,
        logout,
        refreshAuth,
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
