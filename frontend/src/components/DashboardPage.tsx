import { useState, useEffect, useRef } from 'react';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { LogOut, Loader2 } from 'lucide-react';
import { PlatformManager, Platform } from './PlatformManager';
import { TopicStats } from './TopicStats';
import { EmbedCode } from './EmbedCode';
import { api } from '../utils/api';
import grassLogo from '../assets/grass.png';

interface DashboardPageProps {
  userEmail: string;
  onLogout: () => void;
}

// ---------------------------------------------------------
// Iframe 렌더러: jandi_html 고유 스타일 유지
// ---------------------------------------------------------
const GrassIframe = ({ htmlContent }: { htmlContent: string }) => {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // iframe 내부가 투명하게 보이도록 하고, 중앙 정렬만 맞추는 최소한의 스타일
  const minimalCssInjection = `
    <style>
      body { 
        margin: 0 !important; 
        padding: 10px !important; 
        background-color: transparent !important; 
        display: flex;
        justify-content: center;
        overflow: hidden; /* 스크롤바 방지 */
      }
      .container {
        margin: 0 !important;
      }
    </style>
  `;

  // HTML 헤드에 스타일 주입
  const processedHtml = htmlContent.replace('</head>', `${minimalCssInjection}</head>`);

  const adjustHeight = () => {
    const iframe = iframeRef.current;
    if (iframe && iframe.contentWindow) {
      iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 'px';
    }
  };

  return (
    <iframe
      ref={iframeRef}
      title="Grass Widget"
      srcDoc={processedHtml}
      className="w-full border-0 block"
      onLoad={() => {
        adjustHeight();
        setTimeout(adjustHeight, 100);
      }}
    />
  );
};

export function DashboardPage({ userEmail, onLogout }: DashboardPageProps) {
  const [platforms, setPlatforms] = useState<Platform[]>([]);

  const [jandiHtml, setJandiHtml] = useState<string>('');
  const [signedUrl, setSignedUrl] = useState<string>('');
  const [userStats, setUserStats] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAddingPlatform, setIsAddingPlatform] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    setError('');

    try {
      const [stats, userPlatforms] = await Promise.all([
        api.getUserStats(),
        api.getPlatforms(),
      ]);

      try {
        const { url } = await api.getJandiUrl();
        setSignedUrl(url);
        const html = await api.fetchHtml(url);
        setJandiHtml(html);
      } catch (e) {
        console.error('Failed to fetch Jandi HTML:', e);
      }

      setUserStats(stats);
      setPlatforms(userPlatforms);
    } catch (err) {
      console.error('Failed to load data:', err);
      setError(err instanceof Error ? err.message : '데이터를 불러오는데 실패했습니다');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddPlatform = async (platform: string, username: string) => {
    setIsAddingPlatform(true);
    try {
      await api.addPlatform(platform, username);
      loadData();
    } catch (err) {
      console.error('Failed to add platform:', err);
      alert(err instanceof Error ? err.message : '플랫폼 추가에 실패했습니다');
    } finally {
      setIsAddingPlatform(false);
    }
  };

  const handleRemovePlatform = async (platform: string, accountId: string) => {
    if (!confirm('정말로 이 플랫폼 연동을 해제하시겠습니까?')) {
      return;
    }
    try {
      await api.deletePlatform(platform, accountId);
      loadData();
    } catch (err) {
      console.error('Failed to remove platform:', err);
      alert(err instanceof Error ? err.message : '플랫폼 삭제에 실패했습니다');
    }
  };

  return (
    <div className="min-h-screen">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-green-500 to-emerald-600 p-2 rounded-lg">
                <img src={grassLogo} alt="Logo" className="size-6 object-contain invert brightness-0" />
              </div>
              <div>
                <h1 className="text-slate-900">블로그 잔디밭</h1>
                <p className="text-slate-600 text-sm">{userEmail}</p>
              </div>
            </div>
            <Button variant="outline" onClick={onLogout}>
              <LogOut className="size-4 mr-2" />
              로그아웃
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="size-8 animate-spin text-green-600" />
          </div>
        ) : error ? (
          <div className="bg-white p-6 rounded-lg shadow text-center">
            <p className="text-red-600 mb-4">{error}</p>
            <Button onClick={loadData} variant="outline">
              다시 시도
            </Button>
          </div>
        ) : (
          <Tabs defaultValue="grass" className="space-y-6">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="grass">잔디밭</TabsTrigger>
              <TabsTrigger value="platforms">플랫폼 관리</TabsTrigger>
              <TabsTrigger value="embed">임베드</TabsTrigger>
            </TabsList>

            <TabsContent value="grass" className="space-y-6">
              {/* 중복되는 제목(h2) 제거됨 */}

              {jandiHtml && jandiHtml.trim() !== '[]' ? (
                <div className="w-full flex justify-center">
                  <GrassIframe htmlContent={jandiHtml} />
                </div>
              ) : (
                <div className="bg-white p-6 rounded-lg shadow h-32 flex items-center justify-center text-slate-400 text-sm">
                  데이터가 없습니다
                </div>
              )}

              <TopicStats stats={userStats} />
            </TabsContent>

            <TabsContent value="platforms">
              <PlatformManager
                platforms={platforms}
                onAddPlatform={handleAddPlatform}
                onRemovePlatform={handleRemovePlatform}
                isAdding={isAddingPlatform}
              />
            </TabsContent>

            <TabsContent value="embed">
              <EmbedCode userEmail={userEmail} signedUrl={signedUrl} />
            </TabsContent>
          </Tabs>
        )}
      </main>
    </div>
  );
}