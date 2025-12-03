import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Copy, Check, Code2 } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

interface EmbedCodeProps {
  userEmail: string;
  signedUrl: string;
}

export function EmbedCode({ userEmail, signedUrl }: EmbedCodeProps) {
  const [copied, setCopied] = useState(false);

  const userId = userEmail.split('@')[0];
  const baseUrl = 'https://blog-grass.example.com';
  const embedUrl = signedUrl || `${baseUrl}/embed/${userId}`;

  const iframeCode = `<iframe 
  src="${embedUrl}" 
  width="100%" 
  height="350" 
  frameborder="0"
  style="border-radius: 8px;">
</iframe>`;

  const markdownCode = `[Blog Grass](${embedUrl})`;

  const handleCopy = (code: string) => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>잔디밭 임베드하기</CardTitle>
          <CardDescription>
            다른 웹사이트나 블로그에 잔디밭을 임베드할 수 있습니다
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="iframe">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="iframe">iframe</TabsTrigger>
              <TabsTrigger value="notion">Notion</TabsTrigger>
              <TabsTrigger value="markdown">Markdown</TabsTrigger>
            </TabsList>

            <TabsContent value="iframe" className="space-y-4">
              <div>
                <p className="text-slate-700 mb-3">
                  iframe을 사용하여 잔디밭을 임베드합니다. 대부분의 웹사이트에서 사용 가능합니다.
                </p>
                <div className="relative">
                  <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{iframeCode}</code>
                  </pre>
                  <Button
                    size="sm"
                    variant="secondary"
                    className="absolute top-2 right-2"
                    onClick={() => handleCopy(iframeCode)}
                  >
                    {copied ? (
                      <>
                        <Check className="size-4 mr-2" />
                        복사됨
                      </>
                    ) : (
                      <>
                        <Copy className="size-4 mr-2" />
                        복사
                      </>
                    )}
                  </Button>
                </div>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="text-blue-900 flex items-center gap-2 mb-2">
                  <Code2 className="size-4" />
                  사용 방법
                </h4>
                <ul className="text-blue-800 text-sm space-y-1">
                  <li>1. 위 코드를 복사합니다</li>
                  <li>2. 블로그나 웹사이트의 HTML에 붙여넣습니다</li>
                  <li>3. width와 height를 원하는 크기로 조정할 수 있습니다</li>
                </ul>
              </div>
            </TabsContent>

            <TabsContent value="notion" className="space-y-4">
              <div>
                <p className="text-slate-700 mb-3">
                  Notion 페이지에 임베드하려면 아래 링크를 복사하여 붙여넣으세요.
                </p>
                <div className="relative">
                  <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{embedUrl}</code>
                  </pre>
                  <Button
                    size="sm"
                    variant="secondary"
                    className="absolute top-2 right-2"
                    onClick={() => handleCopy(embedUrl)}
                  >
                    {copied ? (
                      <>
                        <Check className="size-4 mr-2" />
                        복사됨
                      </>
                    ) : (
                      <>
                        <Copy className="size-4 mr-2" />
                        복사
                      </>
                    )}
                  </Button>
                </div>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="text-blue-900 flex items-center gap-2 mb-2">
                  <Code2 className="size-4" />
                  사용 방법
                </h4>
                <ul className="text-blue-800 text-sm space-y-1">
                  <li>1. 위 링크를 복사합니다</li>
                  <li>2. Notion 페이지에 붙여넣고 '임베드 생성'을 선택합니다</li>
                </ul>
              </div>
            </TabsContent>

            <TabsContent value="markdown" className="space-y-4">
              <div>
                <p className="text-slate-700 mb-3">
                  GitHub README나 마크다운을 지원하는 플랫폼에서 사용할 수 있습니다.
                </p>
                <div className="relative">
                  <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{markdownCode}</code>
                  </pre>
                  <Button
                    size="sm"
                    variant="secondary"
                    className="absolute top-2 right-2"
                    onClick={() => handleCopy(markdownCode)}
                  >
                    {copied ? (
                      <>
                        <Check className="size-4 mr-2" />
                        복사됨
                      </>
                    ) : (
                      <>
                        <Copy className="size-4 mr-2" />
                        복사
                      </>
                    )}
                  </Button>
                </div>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="text-blue-900 flex items-center gap-2 mb-2">
                  <Code2 className="size-4" />
                  사용 예시
                </h4>
                <ul className="text-blue-800 text-sm space-y-1">
                  <li>• GitHub 프로필 README.md</li>
                  <li>• Velog, Notion 등 마크다운 지원 플랫폼</li>
                  <li>• 클릭하면 전체 잔디밭 페이지로 이동합니다</li>
                </ul>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Preview */}
      <Card>
        <CardHeader>
          <CardTitle>미리보기</CardTitle>
          <CardDescription>
            임베드된 잔디밭이 어떻게 보이는지 확인하세요
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="bg-gradient-to-br from-slate-50 to-slate-100 p-6 rounded-lg border border-slate-200">
            <div className="bg-white rounded-lg p-4 shadow-sm min-h-[350px] flex items-center justify-center">
              {signedUrl ? (
                <iframe
                  src={signedUrl}
                  title="Grass Preview"
                  className="w-full h-[350px] border-0"
                />
              ) : (
                <div className="text-slate-400">
                  미리보기를 불러오는 중...
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
