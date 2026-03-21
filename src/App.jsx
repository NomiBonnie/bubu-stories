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

const storyMap = {
  'story1': story1,
  'story2': story2,
  'story3': story3,
  'story4': story4,
  'story5': story5,
  'story6': story6,
  'story7': story7
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
