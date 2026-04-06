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
  'story20': story20
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
    return <StoryReader story={storyMap[route.id]} storyId={route.id} onBack={() => navigate('/')} />
  }
  return <Home stories={storiesIndex} onSelect={(id) => navigate(`/story/${id}`)} />
}
