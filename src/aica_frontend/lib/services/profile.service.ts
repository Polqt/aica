import { HttpClient } from './http-client';
import { Profile, ProfileUpdate } from '@/lib/types/profile';

export class ProfileService {
  constructor(private httpClient: HttpClient) {}

  async getProfile(): Promise<Profile> {
    return this.httpClient.get<Profile>('/api/v1/profiles/profile');
  }

  async updateProfile(profileData: ProfileUpdate): Promise<Profile> {
    return this.httpClient.put<Profile>(
      '/api/v1/profiles/profile',
      profileData,
    );
  }

  async uploadProfilePicture(file: File): Promise<{ url: string }> {
    const formData = new FormData();
    formData.append('profile_picture', file);

    return this.httpClient.post<{ url: string }>(
      '/api/v1/profiles/profile-picture',
      formData,
      {
        headers: {}, 
      },
    );
  }
}
