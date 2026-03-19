import { useState } from 'react'
import Home from './Home'
import StoryReader from './StoryReader'
import storyData from '../stories/2026-03-19.json'

export default function App() {
  const [reading, setReading] = useState(false)

  if (reading) {
    return <StoryReader story={storyData} onBack={() => setReading(false)} />
  }
  return <Home story={storyData} onStart={() => setReading(true)} />
}
