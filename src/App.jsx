import { useState } from 'react'
import StoryReader from './StoryReader'
import Home from './Home'
import storiesIndex from '../stories/index.json'
import story0319 from '../stories/2026-03-19.json'
import story0320 from '../stories/2026-03-20.json'

const storyMap = {
  '2026-03-19': story0319,
  '2026-03-20': story0320
}

export default function App() {
  const [selectedId, setSelectedId] = useState(null)

  const storyData = selectedId ? storyMap[selectedId] : null

  if (selectedId && storyData) {
    return <StoryReader story={storyData} onBack={() => setSelectedId(null)} />
  }
  return <Home stories={storiesIndex} onSelect={(id) => setSelectedId(id)} />
}
