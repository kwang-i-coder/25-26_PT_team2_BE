import { useEffect, useState } from 'react';
import { OnboardingPage } from './components/OnboardingPage';
import { LoginPage } from './components/LoginPage';
import { SignupPage } from './components/SignupPage';
import { DashboardPage } from './components/DashboardPage';
import { removeToken, setToken, getToken, api } from './utils/api';

export default function App() {
  const [currentPage, setCurrentPage] = useState<'onboarding' | 'login' | 'signup' | 'dashboard'>('onboarding');
  const [userEmail, setUserEmail] = useState('');

  useEffect(() => {
    const token = getToken();
    const storedEmail = localStorage.getItem('userEmail');

    if (token && storedEmail) {
      setUserEmail(storedEmail);
      setCurrentPage('dashboard');
    }
  }, []);

  const handleStartOnboarding = () => {
    setCurrentPage('login');
  };

  const handleGoToSignup = () => {
    setCurrentPage('signup');
  };

  const handleBackToLogin = () => {
    setCurrentPage('login');
  };

  const handleSignup = (email: string, name: string) => {
    setUserEmail(email);
    setCurrentPage('dashboard');
  };

  const handleLogin = async (email: string, password: string) => {
    try {
      const response = await api.signin(email, password);
      setToken(response.access_token);
      setUserEmail(email);
      localStorage.setItem('userEmail', email);
      setCurrentPage('dashboard');
    } catch (error) {
      alert('로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.');
    }
  };

  const handleLogout = () => {
    removeToken();
    localStorage.removeItem('userEmail');
    setCurrentPage('login');
    setUserEmail('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {currentPage === 'onboarding' && (
        <OnboardingPage onStart={handleStartOnboarding} />
      )}
      {currentPage === 'login' && (
        <LoginPage onLogin={handleLogin} onGoToSignup={handleGoToSignup} />
      )}
      {currentPage === 'signup' && (
        <SignupPage onSignup={handleSignup} onBackToLogin={handleBackToLogin} />
      )}
      {currentPage === 'dashboard' && (
        <DashboardPage userEmail={userEmail} onLogout={handleLogout} />
      )}
    </div>
  );
}