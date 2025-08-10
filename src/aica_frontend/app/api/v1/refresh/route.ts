import { NextRequest, NextResponse } from 'next/server';
import { AuthUtils } from '@/lib/auth/utils';
import { UserRepository } from '@/lib/db/user-repository';

export async function POST(request: NextRequest) {
  try {
    // Get refresh token from cookie
    const refreshToken = request.cookies.get('refresh_token')?.value;

    if (!refreshToken) {
      return NextResponse.json(
        { detail: 'Refresh token not found' },
        { status: 401 },
      );
    }

    // Verify refresh token
    const payload = AuthUtils.verifyToken(refreshToken);
    if (!payload) {
      const response = NextResponse.json(
        { detail: 'Invalid or expired refresh token' },
        { status: 401 },
      );

      // Clear invalid refresh token
      response.cookies.set('refresh_token', '', {
        maxAge: 0,
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        path: '/api/v1/refresh',
      });

      return response;
    }

    // Get user from database
    const user = await UserRepository.getUserByEmail(payload.sub);
    if (!user) {
      const response = NextResponse.json(
        { detail: 'User not found' },
        { status: 401 },
      );

      // Clear refresh token for non-existent user
      response.cookies.set('refresh_token', '', {
        maxAge: 0,
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        path: '/api/v1/refresh',
      });

      return response;
    }

    // Generate new access token
    const newAccessToken = AuthUtils.createAccessToken({
      sub: user.email,
      user_id: user.id,
    });

    const expiresIn = 30 * 60; // 30 minutes

    const response = NextResponse.json({
      access_token: newAccessToken,
      token_type: 'bearer',
      expires_in: expiresIn,
    });

    // Set new access token cookie
    response.cookies.set('access_token', `Bearer ${newAccessToken}`, {
      maxAge: expiresIn,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      path: '/',
    });

    return response;
  } catch {
    return NextResponse.json(
      { detail: 'An internal server error occurred during token refresh.' },
      { status: 500 },
    );
  }
}
