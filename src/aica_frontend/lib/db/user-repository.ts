import pool from '../db/connection';
import { AuthUtils } from '../auth/utils';

export interface User {
  id: number;
  email: string;
  hashed_password: string;
  created_at: Date;
}

export interface CreateUserData {
  email: string;
  password: string;
}

export class UserRepository {
  static async getUserByEmail(email: string): Promise<User | null> {
    const client = await pool.connect();
    try {
      const result = await client.query(
        'SELECT id, email, hashed_password, created_at FROM users WHERE email = $1',
        [email],
      );

      if (result.rows.length === 0) {
        return null;
      }

      return result.rows[0] as User;
    } finally {
      client.release();
    }
  }

  static async createUser(userData: CreateUserData): Promise<User> {
    const client = await pool.connect();
    try {
      const sanitizedEmail = AuthUtils.sanitizeEmail(userData.email);
      if (!AuthUtils.validateEmailFormat(sanitizedEmail)) {
        throw new Error('Invalid email format');
      }

      const existingUser = await this.getUserByEmail(sanitizedEmail);
      if (existingUser) {
        throw new Error('User with this email already exists');
      }

      const passwordValidation = AuthUtils.validatePasswordStrength(
        userData.password,
      );
      if (!passwordValidation.isValid) {
        throw new Error(passwordValidation.message);
      }

      const hashedPassword = await AuthUtils.hashPassword(userData.password);

      const result = await client.query(
        'INSERT INTO users (email, hashed_password, created_at) VALUES ($1, $2, NOW()) RETURNING id, email, hashed_password, created_at',
        [sanitizedEmail, hashedPassword],
      );

      return result.rows[0] as User;
    } finally {
      client.release();
    }
  }

  static async authenticateUser(
    email: string,
    password: string,
  ): Promise<User | null> {
    const sanitizedEmail = AuthUtils.sanitizeEmail(email);
    if (!AuthUtils.validateEmailFormat(sanitizedEmail)) {
      return null;
    }

    const user = await this.getUserByEmail(sanitizedEmail);
    if (!user) {
      return null;
    }

    const isValidPassword = await AuthUtils.verifyPassword(
      password,
      user.hashed_password,
    );
    if (!isValidPassword) {
      return null;
    }

    return user;
  }
}
