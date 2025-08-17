import { NextRequest, NextResponse } from 'next/server';
import { UserRepository } from '@/lib/db/user-repository';
import { AuthUtils } from '@/lib/utils/auth';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const username = formData.get('username') as string;
    const password = formData.get('password') as string;

    if (!username || !password) {
      return NextResponse.json(
        { detail: 'Username and password are required' },
        { status: 400 },
      );
    }

    const user = await UserRepository.authenticateUser(username, password);
    if (!user) {
      return NextResponse.json(
        { detail: 'Invalid email or password' },
        { status: 401 },
      );
    }

    const accessToken = AuthUtils.createAccessToken({
      sub: user.email,
      user_id: user.id,
    });

    const expiresIn = 30 * 60; 

    const response = NextResponse.json({
      access_token: accessToken,
      token_type: 'bearer',
      expires_in: expiresIn,
    });
    
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
