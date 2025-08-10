import { NextRequest, NextResponse } from 'next/server';
import { AuthUtils } from '@/lib/auth/utils';
import { UserRepository } from '@/lib/db/user-repository';

function getTokenFromRequest(request: NextRequest): string | null {
  // Try to get token from Authorization header
  const authHeader = request.headers.get('authorization');
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.substring(7);
  }

  // Try to get token from cookie
  const cookieToken = request.cookies.get('access_token')?.value;
  if (cookieToken && cookieToken.startsWith('Bearer ')) {
    return cookieToken.substring(7);
  }

  return null;
}

export async function GET(request: NextRequest) {
  try {
    // Get token from request
    const token = getTokenFromRequest(request);
    if (!token) {
      return NextResponse.json(
        { detail: 'Access token not found' },
        { status: 401 },
      );
    }

    // Verify token
    const payload = AuthUtils.verifyToken(token);
    if (!payload) {
      return NextResponse.json(
        { detail: 'Invalid or expired access token' },
        { status: 401 },
      );
    }

    // Get user from database
    const user = await UserRepository.getUserByEmail(payload.sub);
    if (!user) {
      return NextResponse.json({ detail: 'User not found' }, { status: 401 });
    }

    // Return user info (excluding password)
    return NextResponse.json({
      id: user.id,
      email: user.email,
      created_at: user.created_at,
    });
  } catch {
    return NextResponse.json(
      { detail: 'Failed to retrieve user information' },
      { status: 500 },
    );
  }
}
