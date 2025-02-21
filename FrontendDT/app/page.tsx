"use client"

import { useRef, useState } from "react"
import SimulationWizard from "@/components/SimulationWizard"
import SimulationResults from "@/components/SimulationResults"
import type { SimulationResult } from "@/types"
import HeroSection from "@/components/HeroSection"
import TumorModel from "@/components/TumorModel"
import { ThemeProvider } from "@/components/theme-provider"
import { ModeToggle } from "@/components/mode-toggle"

export default function Home() {
  const [results, setResults] = useState<SimulationResult[] | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Reference for scrolling
  const resultsRef = useRef<HTMLDivElement>(null)

  const handleSimulation = async (patientData: any) => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await fetch("https://digital-twin-your-health-replica.onrender.com/simulate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(patientData),
      })
      if (!response.ok) {
        throw new Error("Failed to fetch simulation results")
      }
      const data = await response.json()
      setResults(data.all_results)

      // Auto-scroll to results
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth" })
      }, 500) // Small delay for smoother experience

    } catch (err) {
      setError("An error occurred while fetching simulation results. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <main className="min-h-screen flex flex-col items-center bg-gradient-to-b from-background to-secondary">
        <div className="container mx-auto px-4 py-12 flex flex-col items-center">
          {/* Mode Toggle */}
          <div className="w-full flex justify-end mb-4">
            <ModeToggle />
          </div>

          {/* Hero Section */}
          <HeroSection />

          {/* Simulation Wizard */}
          <div className="flex flex-col md:flex-row items-center justify-center gap-16 mt-12 w-full">
            <div className="flex-1 flex justify-center">
              <SimulationWizard onSubmit={handleSimulation} isLoading={isLoading} />
            </div>
            <div className="flex-1 flex justify-center">
              <TumorModel />
            </div>
          </div>

          {/* Display errors if any */}
          {error && <p className="text-red-500 mt-4">{error}</p>}

          {/* Simulation Results - Auto Scroll Target */}
          {results && (
            <div ref={resultsRef} className="mt-12 w-full">
              <SimulationResults results={results} />
            </div>
          )}
        </div>
      </main>
    </ThemeProvider>
  )
}

