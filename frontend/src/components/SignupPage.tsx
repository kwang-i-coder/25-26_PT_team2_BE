import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { BookOpen, ArrowLeft, Check, AlertCircle } from 'lucide-react';
import { api } from '../utils/api';
import { Alert, AlertDescription } from './ui/alert';

interface SignupPageProps {
  onSignup: (email: string, name: string) => void;
  onBackToLogin: () => void;
}

export function SignupPage({ onSignup, onBackToLogin }: SignupPageProps) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setError('비밀번호가 일치하지 않습니다');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await api.signup(email, password, name);
      setSuccess(response.message);
      
      // 2초 후 로그인 페이지로 이동
      setTimeout(() => {
        onBackToLogin();
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : '회원가입에 실패했습니다');
    } finally {
      setIsLoading(false);
    }
  };

  const benefits = [
    '여러 블로그 플랫폼 통합 관리',
    'AI 기반 자동 주제 분석',
    '상세한 활동 통계 제공',
    '잔디밭 임베드 코드 생성',
    '무료로 시작하기',
  ];

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-gradient-to-br from-emerald-50 via-white to-green-50">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" />
        <div className="absolute top-40 right-10 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '2s' }} />
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '4s' }} />
      </div>

      <div className="w-full max-w-5xl grid md:grid-cols-2 gap-8 items-center relative z-10">
        {/* Left Side - Benefits */}
        <div className="hidden md:block space-y-6">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-green-500 to-emerald-600 p-3 rounded-xl">
              <BookOpen className="size-8 text-white" />
            </div>
            <div>
              <h1 className="text-slate-900">블로그 잔디밭</h1>
              <p className="text-slate-600">시작하기</p>
            </div>
          </div>

          <div className="space-y-4 bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-green-100">
            <h2 className="text-slate-900 text-2xl">회원가입 혜택</h2>
            <div className="space-y-3">
              {benefits.map((benefit, index) => (
                <div key={index} className="flex items-start gap-3">
                  <div className="mt-1 w-5 h-5 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
                    <Check className="size-3 text-green-600" />
                  </div>
                  <p className="text-slate-700">{benefit}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-6 text-white">
            <p className="text-lg mb-2">✨ 지금 가입하면</p>
            <p className="text-white/90">모든 기능을 무료로 이용하실 수 있습니다</p>
          </div>
        </div>

        {/* Right Side - Signup Form */}
        <div className="space-y-6">
          <div className="md:hidden text-center space-y-2 mb-8">
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="bg-gradient-to-br from-green-500 to-emerald-600 p-3 rounded-xl">
                <BookOpen className="size-8 text-white" />
              </div>
            </div>
            <h1 className="text-slate-900">회원가입</h1>
            <p className="text-slate-600">
              블로그 활동을 시각화하세요
            </p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>계정 만들기</CardTitle>
              <CardDescription>
                이메일로 간편하게 가입하세요
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                {error && (
                  <Alert variant="destructive">
                    <AlertCircle className="size-4" />
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}
                
                {success && (
                  <Alert className="bg-green-50 text-green-900 border-green-200">
                    <Check className="size-4" />
                    <AlertDescription>{success}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-2">
                  <Label htmlFor="name">이름</Label>
                  <Input
                    id="name"
                    type="text"
                    placeholder="홍길동"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="signup-email">이메일</Label>
                  <Input
                    id="signup-email"
                    type="email"
                    placeholder="your@email.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="signup-password">비밀번호</Label>
                  <Input
                    id="signup-password"
                    type="password"
                    placeholder="8자 이상 입력하세요"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={8}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="confirm-password">비밀번호 확인</Label>
                  <Input
                    id="confirm-password"
                    type="password"
                    placeholder="비밀번호를 다시 입력하세요"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                  {confirmPassword && password !== confirmPassword && (
                    <p className="text-red-500 text-sm">비밀번호가 일치하지 않습니다</p>
                  )}
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded-lg p-3">
                  <p className="text-slate-600 text-sm">
                    가입하시면 <button type="button" className="text-green-600 hover:underline">이용약관</button> 및{' '}
                    <button type="button" className="text-green-600 hover:underline">개인정보처리방침</button>에 동의하는 것으로 간주됩니다.
                  </p>
                </div>

                <Button 
                  type="submit" 
                  className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
                  disabled={password !== confirmPassword || isLoading}
                >
                  {isLoading ? '처리 중...' : '회원가입'}
                </Button>
              </form>
              
              <div className="mt-6 pt-6 border-t border-slate-200">
                <Button
                  variant="ghost"
                  onClick={onBackToLogin}
                  className="w-full"
                >
                  <ArrowLeft className="size-4 mr-2" />
                  로그인으로 돌아가기
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}