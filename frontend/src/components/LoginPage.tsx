import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { BookOpen, TrendingUp } from 'lucide-react';

interface LoginPageProps {
  onLogin: (email: string, password: string) => Promise<void>;
  onGoToSignup: () => void;
}

export function LoginPage({ onLogin, onGoToSignup }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (email && password) {
      setIsLoading(true);
      try {
        await onLogin(email, password);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="bg-gradient-to-br from-green-500 to-emerald-600 p-3 rounded-xl">
              <BookOpen className="size-8 text-white" />
            </div>
          </div>
          <h1 className="text-slate-900">블로그 잔디밭</h1>
          <p className="text-slate-600">
            여러 블로그 플랫폼의 글을 한눈에 시각화하세요
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>로그인</CardTitle>
            <CardDescription>
              계정에 로그인하여 블로그 잔디밭을 확인하세요
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">이메일</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="your@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">비밀번호</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? '로그인 중...' : '로그인'}
              </Button>
            </form>

            <div className="mt-6 pt-6 border-t border-slate-200">
              <p className="text-center text-slate-600 text-sm">
                아직 계정이 없으신가요?{' '}
                <button
                  type="button"
                  onClick={onGoToSignup}
                  className="text-green-600 hover:text-green-700"
                >
                  회원가입
                </button>
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="bg-white/50 backdrop-blur-sm rounded-lg p-6 space-y-3">
          <div className="flex items-start gap-3">
            <TrendingUp className="size-5 text-green-600 mt-0.5" />
            <div>
              <p className="text-slate-700">AI 주제 분석</p>
              <p className="text-slate-600 text-sm">
                각 글의 주제를 자동으로 추출하여 색상으로 구분합니다
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}