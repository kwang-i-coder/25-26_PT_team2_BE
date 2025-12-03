const API_HOST = import.meta.env?.VITE_API_HOST || 'localhost';
const API_PORT = import.meta.env?.VITE_API_PORT || '8000';
const BASE_URL = `http://${API_HOST}:${API_PORT}`;

// Token management
export const getToken = (): string | null => {
  const match = document.cookie.match(new RegExp('(^| )access_token=([^;]+)'));
  return match ? match[2] : null;
};

export const setToken = (token: string): void => {
  // Set cookie to expire in 7 days
  const d = new Date();
  d.setTime(d.getTime() + (7 * 24 * 60 * 60 * 1000));
  const expires = "expires=" + d.toUTCString();
  document.cookie = `access_token=${token};${expires};path=/`;
};

export const removeToken = (): void => {
  document.cookie = "access_token=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;";
};

// API client
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const token = getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Auth APIs
  async signup(email: string, password: string, name: string) {
    return this.request<{ message: string }>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    });
  }

  async signin(email: string, password: string) {
    return this.request<{ access_token: string }>('/api/auth/signin', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  // Jandi (Grass) API
  async getJandi(date?: string) {
    const params = date ? `?date=${date}` : '';
    return this.request<Array<{ date: string; topic: string; count: number }>>(
      `/api/jandi${params}`,
      { method: 'GET' }
    );
  }

  async getJandiUrl() {
    return this.request<{ url: string }>('/api/jandi/signedUrl', {
      method: 'GET',
    });
  }

  async fetchHtml(url: string) {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch HTML: ${response.statusText}`);
    }
    return response.text();
  }

  // Platform API
  async addPlatform(platformName: string, accountId: string) {
    return this.request<{ message: string }>('/api/platform', {
      method: 'PUT',
      body: JSON.stringify({ platform_name: platformName, account_id: accountId }),
    });
  }

  async deletePlatform(platformName: string, accountId: string) {
    return this.request<{ message: string }>('/api/platform', {
      method: 'DELETE',
      body: JSON.stringify({ platform_name: platformName, account_id: accountId }),
    });
  }

  async getPlatforms() {
    return this.request<Array<{
      platform_name: string;
      account_id: string;
      last_upload: string | null;
    }>>('/api/platform', {
      method: 'GET',
    });
  }

  // User Stats API
  async getUserStats() {
    return this.request<{
      duration: number;
      category: Array<{ category: string; count: number }>;
      count: number;
      created_at: string;
    }>('/api/user/stats', {
      method: 'GET',
    });
  }

  async getUserPosts(category: string) {
    return this.request<Array<{
      url: string;
      category: string;
      date: string;
      title: string;
      platform: string;
    }>>(`/api/user/posts?category=${encodeURIComponent(category)}`, {
      method: 'GET',
    });
  }
}

export const api = new ApiClient(BASE_URL);