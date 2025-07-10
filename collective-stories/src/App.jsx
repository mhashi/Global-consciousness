import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Globe, Users, BookOpen, Sparkles, Send, Clock, MapPin } from 'lucide-react'
import heroBackground from './assets/Toolpicture1.jpeg'
import thoughtIcon from './assets/Toolpicture1.jpeg'
import './App.css'

function App() {
  const [thought, setThought] = useState('')
  const [isAnonymous, setIsAnonymous] = useState(true)
  const [selectedTags, setSelectedTags] = useState([])

  const availableTags = ['Hope', 'Dreams', 'Love', 'Change', 'Future', 'Peace', 'Growth', 'Connection']

  const currentStory = {
    title: "Echoes of Tomorrow",
    excerpt: "In a world where thoughts traveled faster than light, Maria discovered that her morning coffee ritual connected her to a baker in Tokyo, a student in São Paulo, and a grandmother in Cairo...",
    date: "December 30, 2024",
    contributors: 847
  }

  const recentThoughts = [
    { text: "Sometimes the smallest acts of kindness create the biggest ripples...", location: "Tokyo, Japan", time: "2 min ago" },
    { text: "I wonder if stars dream of the planets they warm...", location: "São Paulo, Brazil", time: "5 min ago" },
    { text: "Every sunrise is a reminder that we get to start again...", location: "Cairo, Egypt", time: "8 min ago" },
    { text: "The sound of rain makes me feel connected to everyone who's ever listened to it...", location: "London, UK", time: "12 min ago" }
  ]

  const pastStories = [
    { title: "The Language of Silence", date: "Dec 23, 2024", contributors: 923 },
    { title: "Bridges Made of Light", date: "Dec 16, 2024", contributors: 756 },
    { title: "The Collector of Moments", date: "Dec 9, 2024", contributors: 834 },
    { title: "When Time Stood Still", date: "Dec 2, 2024", contributors: 692 }
  ]

  const handleTagToggle = (tag) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    )
  }

  const handleSubmit = () => {
    if (thought.trim()) {
      // Here would be the API call to submit the thought
      alert('Thank you for sharing your thought! It will be woven into next week\'s story.')
      setThought('')
      setSelectedTags([])
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="relative z-10 bg-black/20 backdrop-blur-sm border-b border-white/10">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Globe className="h-8 w-8 text-cyan-400" />
              <span className="text-2xl font-bold text-white">Collective Stories</span>
            </div>
            <div className="hidden md:flex space-x-6">
              <a href="#" className="text-white/80 hover:text-white transition-colors">Home</a>
              <a href="#" className="text-white/80 hover:text-white transition-colors">Current Story</a>
              <a href="#" className="text-white/80 hover:text-white transition-colors">Archive</a>
              <a href="#" className="text-white/80 hover:text-white transition-colors">About</a>
            </div>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section 
        className="relative min-h-[70vh] flex items-center justify-center text-center"
        style={{
          backgroundImage: `url(${heroBackground})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundAttachment: 'fixed'
        }}
      >
        <div className="absolute inset-0 bg-black/40"></div>
        <div className="relative z-10 container mx-auto px-4">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            Where Global Thoughts
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
              Become Stories
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-white/90 mb-8 max-w-3xl mx-auto">
            Every week, your ideas and thoughts from around the world are woven into a unique short story, 
            reflecting our shared human consciousness.
          </p>
          <Button 
            size="lg" 
            className="bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white px-8 py-3 text-lg"
            onClick={() => document.getElementById('submit-section').scrollIntoView({ behavior: 'smooth' })}
          >
            <Sparkles className="mr-2 h-5 w-5" />
            Share Your Thought
          </Button>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12 space-y-16">
        {/* Current Story Section */}
        <section className="text-center">
          <h2 className="text-4xl font-bold text-white mb-8">This Week's Story</h2>
          <Card className="max-w-4xl mx-auto bg-white/10 backdrop-blur-sm border-white/20">
            <CardHeader>
              <CardTitle className="text-2xl text-white">{currentStory.title}</CardTitle>
              <CardDescription className="text-white/70 flex items-center justify-center space-x-4">
                <span className="flex items-center">
                  <Clock className="mr-1 h-4 w-4" />
                  {currentStory.date}
                </span>
                <span className="flex items-center">
                  <Users className="mr-1 h-4 w-4" />
                  {currentStory.contributors} contributors
                </span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-white/90 text-lg leading-relaxed mb-6">
                {currentStory.excerpt}
              </p>
              <Button variant="outline" className="border-white/30 text-white hover:bg-white/10">
                <BookOpen className="mr-2 h-4 w-4" />
                Read Full Story
              </Button>
            </CardContent>
          </Card>
        </section>

        {/* Submission Section */}
        <section id="submit-section" className="max-w-2xl mx-auto">
          <div className="text-center mb-8">
            <img src={thoughtIcon} alt="Thought" className="w-16 h-16 mx-auto mb-4 opacity-80" />
            <h2 className="text-4xl font-bold text-white mb-4">Add Your Voice to the Collective</h2>
            <p className="text-white/70 text-lg">
              Share a thought, idea, or feeling. It might inspire next week's story.
            </p>
          </div>
          
          <Card className="bg-white/10 backdrop-blur-sm border-white/20">
            <CardContent className="p-6 space-y-6">
              <div>
                <Textarea
                  placeholder="What's on your mind? Share a thought, dream, observation, or feeling..."
                  value={thought}
                  onChange={(e) => setThought(e.target.value)}
                  className="min-h-32 bg-white/5 border-white/20 text-white placeholder:text-white/50 resize-none"
                  maxLength={500}
                />
                <div className="text-right text-sm text-white/50 mt-2">
                  {thought.length}/500 characters
                </div>
              </div>

              <div>
                <label className="text-white/80 text-sm font-medium mb-3 block">
                  Tags (optional)
                </label>
                <div className="flex flex-wrap gap-2">
                  {availableTags.map(tag => (
                    <Badge
                      key={tag}
                      variant={selectedTags.includes(tag) ? "default" : "outline"}
                      className={`cursor-pointer transition-all ${
                        selectedTags.includes(tag)
                          ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white'
                          : 'border-white/30 text-white/70 hover:bg-white/10'
                      }`}
                      onClick={() => handleTagToggle(tag)}
                    >
                      {tag}
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="anonymous"
                  checked={isAnonymous}
                  onChange={(e) => setIsAnonymous(e.target.checked)}
                  className="rounded border-white/30"
                />
                <label htmlFor="anonymous" className="text-white/80 text-sm">
                  Submit anonymously
                </label>
              </div>

              <Button 
                onClick={handleSubmit}
                disabled={!thought.trim()}
                className="w-full bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 disabled:opacity-50"
              >
                <Send className="mr-2 h-4 w-4" />
                Share Your Thought
              </Button>
            </CardContent>
          </Card>
        </section>

        {/* Recent Activity */}
        <section>
          <h2 className="text-4xl font-bold text-white text-center mb-8">Recent Thoughts from Around the World</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {recentThoughts.map((item, index) => (
              <Card key={index} className="bg-white/5 backdrop-blur-sm border-white/10 hover:bg-white/10 transition-all">
                <CardContent className="p-4">
                  <p className="text-white/90 mb-3 italic">"{item.text}"</p>
                  <div className="flex items-center justify-between text-sm text-white/60">
                    <span className="flex items-center">
                      <MapPin className="mr-1 h-3 w-3" />
                      {item.location}
                    </span>
                    <span>{item.time}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Story Archive */}
        <section>
          <h2 className="text-4xl font-bold text-white text-center mb-8">Past Stories</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {pastStories.map((story, index) => (
              <Card key={index} className="bg-white/5 backdrop-blur-sm border-white/10 hover:bg-white/10 transition-all cursor-pointer">
                <CardHeader>
                  <CardTitle className="text-white text-lg">{story.title}</CardTitle>
                  <CardDescription className="text-white/60">
                    <div className="flex items-center justify-between">
                      <span>{story.date}</span>
                      <span className="flex items-center">
                        <Users className="mr-1 h-3 w-3" />
                        {story.contributors}
                      </span>
                    </div>
                  </CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
          <div className="text-center mt-8">
            <Button variant="outline" className="border-white/30 text-white hover:bg-white/10">
              View All Stories
            </Button>
          </div>
        </section>

        {/* Stats Section */}
        <section className="text-center py-12">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="text-4xl font-bold text-cyan-400 mb-2">12,847</div>
              <div className="text-white/70">Thoughts Shared</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-400 mb-2">52</div>
              <div className="text-white/70">Stories Created</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-yellow-400 mb-2">127</div>
              <div className="text-white/70">Countries Represented</div>
            </div>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="bg-black/30 backdrop-blur-sm border-t border-white/10 py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-white/70 mb-4">
            Collective Stories - Where humanity's shared consciousness creates art
          </p>
          <p className="text-white/50 text-sm">
            Every thought matters. Every voice counts. Every story connects us.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App

