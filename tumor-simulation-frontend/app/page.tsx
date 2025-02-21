"use client"

import { useState } from "react"
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
    } catch (err) {
      setError("An error occurred while fetching simulation results. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <main className="min-h-screen bg-gradient-to-b from-background to-secondary">
        <div className="container mx-auto px-4 py-8">
          <div className="flex justify-end mb-4">
            <ModeToggle />
          </div>
          <HeroSection />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12">
            <div>
              <SimulationWizard onSubmit={handleSimulation} isLoading={isLoading} />
              {error && <p className="text-red-500 mt-4">{error}</p>}
            </div>
            <div className="flex items-center justify-center">
              <TumorModel />
            </div>
          </div>
          {results && <SimulationResults results={results} />}
        </div>
      </main>
    </ThemeProvider>
  )
}

