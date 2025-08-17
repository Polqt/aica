import { NextRequest, NextResponse } from 'next/server';
import { UserRepository } from '@/lib/db/user-repository';
import { AuthUtils } from '@/lib/utils/auth';

export async function POST(request: NextRequest) {
  try {
    const refreshToken = request.cookies.get('refresh_token')?.value;

    if (!refreshToken) {
      return NextResponse.json(
        { detail: 'Refresh token not found' },
        { status: 401 },
      );
    }

    const payload = AuthUtils.verifyToken(refreshToken);
    if (!payload) {
      const response = NextResponse.json(
        { detail: 'Invalid or expired refresh token' },
        { status: 401 },
      );

      response.cookies.set('refresh_token', '', {
        maxAge: 0,
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        path: '/api/v1/refresh',
      });

      return response;
    }

    const user = await UserRepository.getUserByEmail(payload.sub);
    if (!user) {
      const response = NextResponse.json(
        { detail: 'User not found' },
        { status: 401 },
      );

      response.cookies.set('refresh_token', '', {
        maxAge: 0,
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        path: '/api/v1/refresh',
      });

      return response;
    }

    const newAccessToken = AuthUtils.createAccessToken({
      sub: user.email,
      user_id: user.id,
    });

    const expiresIn = 30 * 60; 

    const response = NextResponse.json({
      access_token: newAccessToken,
      token_type: 'bearer',
      expires_in: expiresIn,
    });

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
