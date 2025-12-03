import { Button } from './ui/button';
import { ArrowRight, Sparkles, BarChart3, Share2 } from 'lucide-react';
import velogIcon from '../assets/velog.png';
import tistoryIcon from '../assets/tistory.webp';
import naverIcon from '../assets/naver_blog.svg';
import grassLogo from '../assets/grass.png';

interface OnboardingPageProps {
  onStart: () => void;
}

const FloatingIcon = ({
  icon,
  delay,
  duration,
  startX,
  startY
}: {
  icon: string;
  delay: number;
  duration: number;
  startX: string;
  startY: string;
}) => (
  <div
    className="absolute text-4xl opacity-20 animate-float"
    style={{
      left: startX,
      top: startY,
      animationDelay: `${delay}s`,
      animationDuration: `${duration}s`,
    }}
  >
    {icon}
  </div>
);

export function OnboardingPage({ onStart }: OnboardingPageProps) {
  const blogIcons = [
    { icon: '📝', label: 'Tistory' },
    { icon: '🟢', label: 'Naver' },
    { icon: '💚', label: 'Velog' },
    { icon: '📖', label: 'Blog' },
    { icon: '✍️', label: 'Write' },
    { icon: '🌿', label: 'Grass' },
    { icon: '📊', label: 'Stats' },
    { icon: '🎨', label: 'Design' },
    { icon: '🚀', label: 'Launch' },
    { icon: '⭐', label: 'Star' },
  ];

  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-emerald-50 via-white to-green-50">
      {/* Floating Blog Icons Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {blogIcons.map((item, index) => (
          <FloatingIcon
            key={index}
            icon={item.icon}
            delay={index * 0.5}
            duration={15 + (index % 5) * 2}
            startX={`${(index * 17) % 90}%`}
            startY={`${(index * 23) % 90}%`}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 min-h-screen flex items-center justify-center p-4">
        <div className="max-w-4xl w-full">
          <div className="text-center space-y-8">
            {/* Logo & Title */}
            <div className="space-y-4">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl shadow-2xl mb-4 animate-bounce-slow">
                <img src={grassLogo} alt="Logo" className="size-12 object-contain invert brightness-0" />
              </div>
              <h1 className="text-slate-900 text-5xl sm:text-6xl md:text-7xl tracking-tight">
                블로그 잔디밭
              </h1>
              <p className="text-slate-600 text-xl sm:text-2xl max-w-2xl mx-auto">
                여러 플랫폼의 블로그 활동을 한눈에 시각화하고
                <br />
                AI로 주제를 분석하세요
              </p>
            </div>

            {/* Feature Cards */}
            <div className="grid md:grid-cols-3 gap-6 max-w-3xl mx-auto mt-12">
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-green-100 hover:scale-105 transition-transform">
                <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-emerald-500 rounded-xl flex items-center justify-center mb-4 mx-auto">
                  <Sparkles className="size-6 text-white" />
                </div>
                <h3 className="text-slate-900 mb-2">AI 주제 분석</h3>
                <p className="text-slate-600 text-sm">
                  각 글의 주제를 자동으로 추출하여 색상으로 구분합니다
                </p>
              </div>

              <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-blue-100 hover:scale-105 transition-transform">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-blue-500 rounded-xl flex items-center justify-center mb-4 mx-auto">
                  <BarChart3 className="size-6 text-white" />
                </div>
                <h3 className="text-slate-900 mb-2">상세한 통계</h3>
                <p className="text-slate-600 text-sm">
                  작성한 글의 주제별 분포와 활동 패턴을 확인하세요
                </p>
              </div>

              <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-purple-100 hover:scale-105 transition-transform">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-purple-500 rounded-xl flex items-center justify-center mb-4 mx-auto">
                  <Share2 className="size-6 text-white" />
                </div>
                <h3 className="text-slate-900 mb-2">간편한 공유</h3>
                <p className="text-slate-600 text-sm">
                  iframe 코드로 다른 곳에 잔디밭을 임베드하세요
                </p>
              </div>
            </div>

            {/* CTA Button */}
            <div className="pt-8">
              <Button
                onClick={onStart}
                size="lg"
                className="text-lg px-8 py-6 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 shadow-xl hover:shadow-2xl transition-all"
              >
                시작하기
                <ArrowRight className="size-5 ml-2" />
              </Button>
            </div>

            {/* Supported Platforms */}
            <div className="pt-8">
              <p className="text-slate-500 text-sm mb-4">지원하는 플랫폼</p>
              <div className="flex items-center justify-center gap-6 flex-wrap">
                <div className="flex items-center gap-2 bg-white/60 px-4 py-2 rounded-full">
                  <img src={tistoryIcon} alt="Tistory" className="h-5 w-auto object-contain" />
                  <span className="text-slate-700 text-sm">티스토리</span>
                </div>
                <div className="flex items-center gap-2 bg-white/60 px-4 py-2 rounded-full">
                  <img src={naverIcon} alt="Naver" className="h-5 w-auto object-contain" />
                  <span className="text-slate-700 text-sm">네이버</span>
                </div>
                <div className="flex items-center gap-2 bg-white/60 px-4 py-2 rounded-full">
                  <img src={velogIcon} alt="Velog" className="h-5 w-auto object-contain" />
                  <span className="text-slate-700 text-sm">Velog</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Gradient */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white/50 to-transparent pointer-events-none" />
    </div>
  );
}
