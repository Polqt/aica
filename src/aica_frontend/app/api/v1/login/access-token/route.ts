import { NextRequest, NextResponse } from 'next/server';
import { UserRepository } from '@/lib/db/user-repository';
import { AuthUtils } from '@/lib/auth/utils';

export async function POST(request: NextRequest) {
  try {
    // Handle form data (like OAuth2PasswordRequestForm)
    const formData = await request.formData();
    const username = formData.get('username') as string;
    const password = formData.get('password') as string;

    if (!username || !password) {
      return NextResponse.json(
        { detail: 'Username and password are required' },
        { status: 400 },
      );
    }

    // Authenticate user (validation happens in UserRepository)
    const user = await UserRepository.authenticateUser(username, password);
    if (!user) {
      return NextResponse.json(
        { detail: 'Invalid email or password' },
        { status: 401 },
      );
    }

    // Generate tokens
    const accessToken = AuthUtils.createAccessToken({
      sub: user.email,
      user_id: user.id,
    });

    const expiresIn = 30 * 60; // 30 minutes in seconds

    // Create response with cookies
    const response = NextResponse.json({
      access_token: accessToken,
      token_type: 'bearer',
      expires_in: expiresIn,
    });

    // Set cookies
    response.cookies.set('access_token', `Bearer ${accessToken}`, {
      maxAge: expiresIn,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      path: '/',
    });

    return response;
  } catch {
    return NextResponse.json(
      { detail: 'An internal server error occurred during login.' },
      { status: 500 },
    );
  }
}
