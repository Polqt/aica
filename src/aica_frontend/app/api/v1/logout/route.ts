import { NextResponse } from 'next/server';

export async function POST() {
  try {
    const response = NextResponse.json({
      message: 'Successfully logged out',
    });

    response.cookies.set('access_token', '', {
      maxAge: 0,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      path: '/',
    });

    response.cookies.set('refresh_token', '', {
      maxAge: 0,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      path: '/api/v1/refresh',
    });

    return response;
  } catch {
    return NextResponse.json(
      { detail: 'An internal server error occurred during logout.' },
      { status: 500 },
    );
  }
}
