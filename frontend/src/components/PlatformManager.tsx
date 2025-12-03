import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Trash2, Plus, Loader2 } from 'lucide-react';
import { Badge } from './ui/badge';
import velogIcon from '../assets/velog.png';
import tistoryIcon from '../assets/tistory.webp';
import naverIcon from '../assets/naver_blog.svg';

export interface Platform {
  platform_name: string;
  account_id: string;
  last_upload: string | null;
}

interface PlatformManagerProps {
  platforms: Platform[];
  onAddPlatform: (platform: string, username: string) => void;
  onRemovePlatform: (platform: string, accountId: string) => void;
  isAdding?: boolean;
}

const PLATFORM_OPTIONS = [
  { value: 'tistory', label: '티스토리', icon: tistoryIcon },
  { value: 'naver', label: '네이버 블로그', icon: naverIcon },
  { value: 'velog', label: 'Velog', icon: velogIcon },
];

export function PlatformManager({ platforms, onAddPlatform, onRemovePlatform, isAdding = false }: PlatformManagerProps) {
  const [selectedPlatform, setSelectedPlatform] = useState('');
  const [username, setUsername] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedPlatform && username) {
      onAddPlatform(selectedPlatform, username);
      setSelectedPlatform('');
      setUsername('');
    }
  };

  const getPlatformLabel = (platform: string) => {
    return PLATFORM_OPTIONS.find(p => p.value === platform)?.label || platform;
  };

  const getPlatformIcon = (platform: string) => {
    return PLATFORM_OPTIONS.find(p => p.value === platform)?.icon || '📄';
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>플랫폼 추가</CardTitle>
          <CardDescription>
            연동할 블로그 플랫폼과 사용자 ID를 입력하세요
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="platform">플랫폼 선택</Label>
                <Select value={selectedPlatform} onValueChange={setSelectedPlatform}>
                  <SelectTrigger id="platform">
                    <SelectValue placeholder="플랫폼을 선택하세요" />
                  </SelectTrigger>
                  <SelectContent>
                    {PLATFORM_OPTIONS.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        <span className="flex items-center gap-2">
                          <img src={option.icon} alt={option.label} className="w-12 h-6 object-contain rounded-sm" />
                          <span>{option.label}</span>
                        </span>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="username">블로그 ID / 사용자명</Label>
                <Input
                  id="username"
                  placeholder="예: my-blog"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
            </div>
            <div className="flex items-center gap-3 flex-wrap">
              <Button type="submit" className="w-full sm:w-auto" disabled={isAdding}>
                {isAdding ? (
                  <>
                    <Loader2 className="size-4 mr-2 animate-spin" />
                    추가 중...
                  </>
                ) : (
                  <>
                    <Plus className="size-4 mr-2" />
                    플랫폼 추가
                  </>
                )}
              </Button>
              <p className="text-xs text-slate-500">
                * 플랫폼 추가시 동기화에 시간이 걸릴 수 있습니다.
              </p>
            </div>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>연동된 플랫폼</CardTitle>
          <CardDescription>
            현재 연동되어 있는 블로그 플랫폼 목록입니다
          </CardDescription>
        </CardHeader>
        <CardContent>
          {platforms.length === 0 ? (
            <div className="text-center py-8 text-slate-500">
              연동된 플랫폼이 없습니다. 위에서 플랫폼을 추가해주세요.
            </div>
          ) : (
            <div className="space-y-3">
              {platforms.map((platform, index) => (
                <div
                  key={`${platform.platform_name}-${platform.account_id}-${index}`}
                  className="flex items-center justify-between p-4 bg-slate-50 rounded-lg border border-slate-200"
                >
                  <div className="flex items-center gap-3">
                    <div className="h-8 w-12 flex items-center justify-center bg-white rounded-lg border border-slate-100 p-1">
                      <img
                        src={getPlatformIcon(platform.platform_name)}
                        alt={platform.platform_name}
                        className="w-full h-full object-contain"
                      />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-slate-900">{platform.account_id}</span>
                        <Badge variant="secondary">
                          {getPlatformLabel(platform.platform_name)}
                        </Badge>
                      </div>
                      {platform.last_upload && (
                        <p className="text-slate-600 text-sm">
                          마지막 업로드: {new Date(platform.last_upload).toLocaleDateString()}
                        </p>
                      )}
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onRemovePlatform(platform.platform_name, platform.account_id)}
                  >
                    <Trash2 className="size-4 text-red-500" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
