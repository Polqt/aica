import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const SECRET_KEY = process.env.SECRET_KEY || 'your-secret-key';
const ACCESS_TOKEN_EXPIRE_MINUTES = 30;

export class AuthUtils {
  static async hashPassword(password: string): Promise<string> {
    const saltRounds = parseInt(process.env.PASSWORD_HASH_ROUNDS || '12');
    return bcrypt.hash(password, saltRounds);
  }

  static async verifyPassword(
    password: string,
    hashedPassword: string,
  ): Promise<boolean> {
    return bcrypt.compare(password, hashedPassword);
  }

  static createAccessToken(data: { sub: string; user_id: number }): string {
    const expiresIn = ACCESS_TOKEN_EXPIRE_MINUTES * 60;
    return jwt.sign(data, SECRET_KEY, {
      expiresIn: `${expiresIn}s`,
      algorithm: 'HS256',
    });
  }

  static verifyToken(token: string): { sub: string; user_id: number } | null {
    try {
      return jwt.verify(token, SECRET_KEY) as { sub: string; user_id: number };
    } catch {
      return null;
    }
  }

  static validateEmailFormat(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  static sanitizeEmail(email: string): string {
    return email.toLowerCase().trim();
  }

  static validatePasswordStrength(password: string): {
    isValid: boolean;
    message: string;
  } {
    const minLength = parseInt(process.env.MIN_PASSWORD_LENGTH || '8');
    const maxLength = parseInt(process.env.MAX_PASSWORD_LENGTH || '128');
    const requireSpecialChars = process.env.REQUIRE_SPECIAL_CHARS === 'true';

    if (password.length < minLength) {
      return {
        isValid: false,
        message: `Password must be at least ${minLength} characters long`,
      };
    }

    if (password.length > maxLength) {
      return {
        isValid: false,
        message: `Password must be no more than ${maxLength} characters long`,
      };
    }

    if (!/(?=.*[a-z])/.test(password)) {
      return {
        isValid: false,
        message: 'Password must contain at least one lowercase letter',
      };
    }

    if (!/(?=.*[A-Z])/.test(password)) {
      return {
        isValid: false,
        message: 'Password must contain at least one uppercase letter',
      };
    }

    if (!/(?=.*\d)/.test(password)) {
      return {
        isValid: false,
        message: 'Password must contain at least one number',
      };
    }

    if (
      requireSpecialChars &&
      !/(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?])/.test(password)
    ) {
      return {
        isValid: false,
        message: 'Password must contain at least one special character',
      };
    }

    return { isValid: true, message: 'Password is valid' };
  }
}
