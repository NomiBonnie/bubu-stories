import { useState, useEffect } from 'react'
import StoryReader from './StoryReader'
import Home from './Home'
import storiesIndex from '../stories/index.json'
import story1 from '../stories/story1.json'
import story2 from '../stories/story2.json'
import story3 from '../stories/story3.json'
import story4 from '../stories/story4.json'
import story5 from '../stories/story5.json'
import story6 from '../stories/story6.json'
import story7 from '../stories/story7.json'
import story8 from '../stories/story8.json'
import story9 from '../stories/story9.json'
import story10 from '../stories/story10.json'
import story11 from '../stories/story11.json'
import story12 from '../stories/story12.json'
import story13 from '../stories/story13.json'
import story14 from '../stories/story14.json'
import story15 from '../stories/story15.json'
import story16 from '../stories/story16.json'
import story17 from '../stories/story17.json'
import story18 from '../stories/story18.json'
import story19 from '../stories/story19.json'
import story20 from '../stories/story20.json'
import story21 from '../stories/story21.json'
import story22 from '../stories/story22.json'
import story23 from '../stories/story23.json'
import story24 from '../stories/story24.json'
import story25 from '../stories/story25.json'
import story26 from '../stories/story26.json'
import story27 from '../stories/story27.json'
import story28 from '../stories/story28.json'
import story29 from '../stories/story29.json'
import story30 from '../stories/story30.json'
import story31 from '../stories/story31.json'
import story32 from '../stories/story32.json'
import story33 from '../stories/story33.json'
import story34 from '../stories/story34.json'
import story35 from '../stories/story35.json'

const storyMap = {
  'story1': story1,
  'story2': story2,
  'story3': story3,
  'story4': story4,
  'story5': story5,
  'story6': story6,
  'story7': story7,
  'story8': story8,
  'story9': story9,
  'story10': story10,
  'story11': story11,
  'story12': story12,
  'story13': story13,
  'story14': story14,
  'story15': story15,
  'story16': story16,
  'story17': story17,
  'story18': story18,
  'story19': story19,
  'story20': story20,
  'story21': story21,
  'story22': story22,
  'story23': story23,
  'story24': story24,
  'story25': story25,
  'story26': story26,
  'story27': story27,
  'story28': story28,
  'story29': story29,
  'story30': story30,
  'story31': story31,
  'story32': story32,
  'story33': story33,
  'story34': story34,
  'story35': story35
}

function getRoute() {
  const hash = window.location.hash.replace('#', '')
  if (hash.startsWith('/story/')) {
    return { view: 'story', id: hash.replace('/story/', '') }
  }
  return { view: 'home' }
}

export default function App() {
  const [route, setRoute] = useState(getRoute)
  const [lang, setLang] = useState(() => localStorage.getItem('bubu-lang') || 'zh')

  const toggleLang = () => {
    setLang(prev => {
      const next = prev === 'zh' ? 'en' : 'zh'
      localStorage.setItem('bubu-lang', next)
      return next
    })
  }

  useEffect(() => {
    const handler = () => setRoute(getRoute())
    window.addEventListener('hashchange', handler)
    return () => window.removeEventListener('hashchange', handler)
  }, [])

  useEffect(() => {
    const meta = document.getElementById('theme-color')
    if (meta) {
      meta.setAttribute('content', route.view === 'story' ? '#0D0B09' : '#FAF8F5')
    }
    document.body.style.background = route.view === 'story' ? '#0D0B09' : '#FAF8F5'
  }, [route.view])

  const navigate = (path) => {
    window.location.hash = path
  }

  if (route.view === 'story' && storyMap[route.id]) {
    return <StoryReader story={storyMap[route.id]} storyId={route.id} onBack={() => navigate('/')} lang={lang} toggleLang={toggleLang} />
  }
  const sortedStories = [...storiesIndex].sort((a, b) => (b.chapter || 0) - (a.chapter || 0))
  return <Home stories={sortedStories} onSelect={(id) => navigate(`/story/${id}`)} lang={lang} toggleLang={toggleLang} />
}
