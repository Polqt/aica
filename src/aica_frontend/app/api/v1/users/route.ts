import { NextRequest, NextResponse } from 'next/server';
import { UserRepository } from '@/lib/db/user-repository';
import { AuthUtils } from '@/lib/auth/utils';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, password } = body;

    if (!email || !password) {
      return NextResponse.json(
        { detail: 'Email and password are required' },
        { status: 400 },
      );
    }

    // Create user
    const newUser = await UserRepository.createUser({ email, password });

    // Generate token
    const accessToken = AuthUtils.createAccessToken({
      sub: newUser.email,
      user_id: newUser.id,
    });

    return NextResponse.json({
      access_token: accessToken,
      token_type: 'bearer',
    });
  } catch (error) {
    if (error instanceof Error) {
      if (
        error.message.includes('already exists') ||
        error.message.includes('Invalid email') ||
        error.message.includes('Password must')
      ) {
        return NextResponse.json({ detail: error.message }, { status: 400 });
      }
    }

    return NextResponse.json(
      { detail: 'An internal server error occurred during registration.' },
      { status: 500 },
    );
  }
}
