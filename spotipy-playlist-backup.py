import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# 1) 환경변수에서 Client 정보 불러오기
client_id     = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
if not client_id or not client_secret:
    raise RuntimeError("SPOTIPY_CLIENT_ID / SECRET 환경변수 설정 필요")

# 2) Client Credentials 인증
auth_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
sp = Spotify(auth_manager=auth_manager)

# 3) 플레이리스트 ID (URL 중간 부분)
playlist_id = '0EWazPeaznzh1Cydl0PH7g'

tracks = []
# 4) 첫 페이지 가져오기 (limit 최대 100)
results = sp.playlist_items(
    playlist_id,
    fields='items.track.name,items.track.artists(name),next',
    additional_types=['track'],
    limit=100
)

# 5) 페이지네이션 처리
while results:
    for item in results['items']:
        track = item.get('track')
        if track:
            name    = track['name']
            artists = ', '.join(a['name'] for a in track['artists'])
            tracks.append(f'{artists} - {name}')
    # 다음 페이지가 있으면 이어서 요청
    if results.get('next'):
        results = sp.next(results)
    else:
        break

# 6) 결과 출력 및 파일 저장
print(f'총 {len(tracks)}곡 추출됨\n')
for i, t in enumerate(tracks, 1):
    print(f'{i}. {t}')

with open('playlist_tracks.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(tracks))

print("\n→ playlist_tracks.txt에 저장되었습니다.")
