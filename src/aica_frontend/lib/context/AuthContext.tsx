'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { apiClient } from '@/lib/services/api-client';
import { TokenManager } from '@/lib/utils/token-manager';

interface AuthContextProps {
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  setAuthToken: (token: string) => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = () => {
      const hasToken = TokenManager.hasValidToken();
      setIsAuthenticated(hasToken);
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const setAuthToken = (token: string) => {
    TokenManager.setAccessToken(token);
    setIsAuthenticated(true);
  };

  const login = async (email: string, password: string): Promise<void> => {
    setIsLoading(true);

    try {
      await apiClient.auth.login({ email, password });


      setIsAuthenticated(true);
    } catch (error) {
      setIsAuthenticated(false);
      throw error; 
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);

    try {
      await apiClient.auth.logout();
    } catch (error) {
      console.warn('Logout request failed:', error);
    } finally {
      setIsAuthenticated(false);
      setIsLoading(false);
    }
  };

  const contextValue: AuthContextProps = {
    isAuthenticated,
    isLoading,
    login,
    logout,
    setAuthToken,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextProps => {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};
