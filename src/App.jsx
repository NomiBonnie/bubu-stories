import { useState, useEffect } from 'react'
import StoryReader from './StoryReader'
import Home from './Home'
import storiesIndex from '../stories/index.json'
import story0319 from '../stories/2026-03-19.json'
import story0320 from '../stories/2026-03-20.json'
import story0321 from '../stories/2026-03-21.json'
import story0322 from '../stories/2026-03-22.json'

const storyMap = {
  '2026-03-19': story0319,
  '2026-03-20': story0320,
  '2026-03-21': story0321,
  '2026-03-22': story0322
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

  const navigate = (path) => {
    window.location.hash = path
  }

  if (route.view === 'story' && storyMap[route.id]) {
    return <StoryReader story={storyMap[route.id]} onBack={() => navigate('/')} />
  }
  return <Home stories={storiesIndex} onSelect={(id) => navigate(`/story/${id}`)} />
}
