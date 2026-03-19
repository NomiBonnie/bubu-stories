import { useState } from 'react'
import StoryReader from './StoryReader'
import Home from './Home'
import storiesIndex from '../stories/index.json'
import storyData2026 from '../stories/2026-03-19.json'

const storyMap = {
  '2026-03-19': storyData2026
}

export default function App() {
  const [selectedId, setSelectedId] = useState(null)

  const storyData = selectedId ? storyMap[selectedId] : null

  if (selectedId && storyData) {
    return <StoryReader story={storyData} onBack={() => setSelectedId(null)} />
  }
  return <Home stories={storiesIndex} onSelect={(id) => setSelectedId(id)} />
}
