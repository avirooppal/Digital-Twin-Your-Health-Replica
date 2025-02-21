"use client"

import type { SimulationResult } from "@/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Bar, BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"
import { motion } from "framer-motion"

interface SimulationResultsProps {
  results: SimulationResult[]
}

export default function SimulationResults({ results }: SimulationResultsProps) {
  const bestTreatment = results[0]

  const chartData = results.map((result) => ({
    name: result.drug,
    "Tumor Reduction": result.tumor_reduction_percent,
    "Side Effects Risk": result.side_effects_risk,
  }))

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="mt-8 space-y-6"
    >
      <h2 className="text-2xl font-bold">Simulation Results</h2>
      <Card className="bg-primary/5">
        <CardHeader>
          <CardTitle>Best Treatment</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="font-semibold">Drug:</p>
              <p>{bestTreatment.drug}</p>
            </div>
            <div>
              <p className="font-semibold">Dose:</p>
              <p>{bestTreatment.dose} mg</p>
            </div>
            <div>
              <p className="font-semibold">Final Tumor Size:</p>
              <p>{bestTreatment.final_tumor_size} mm³</p>
            </div>
            <div>
              <p className="font-semibold">Tumor Reduction:</p>
              <p>{bestTreatment.tumor_reduction_percent}%</p>
            </div>
            <div>
              <p className="font-semibold">Time to Half Size:</p>
              <p>{bestTreatment.time_to_half_size ? `${bestTreatment.time_to_half_size} days` : "N/A"}</p>
            </div>
            <div>
              <p className="font-semibold">Sustained Effect:</p>
              <p>{bestTreatment.sustained_effect ? "Yes" : "No"}</p>
            </div>
            <div>
              <p className="font-semibold">Side Effects Risk:</p>
              <p>{bestTreatment.side_effects_risk}%</p>
            </div>
            <div>
              <p className="font-semibold">Ranking Score:</p>
              <p>{bestTreatment.ranking_score}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <h3 className="text-xl font-semibold mt-6 mb-4">Treatment Comparison</h3>
      <Card>
        <CardContent className="pt-6">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="Tumor Reduction" fill="#8884d8" />
              <Bar dataKey="Side Effects Risk" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <h3 className="text-xl font-semibold mt-6 mb-4">All Results</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {results.map((result, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle>{result.drug}</CardTitle>
            </CardHeader>
            <CardContent>
              <p>Dose: {result.dose} mg</p>
              <p>Final Tumor Size: {result.final_tumor_size} mm³</p>
              <p>Tumor Reduction: {result.tumor_reduction_percent}%</p>
              <Progress value={result.tumor_reduction_percent} className="mt-2" />
              <p>Time to Half Size: {result.time_to_half_size ? `${result.time_to_half_size} days` : "N/A"}</p>
              <p>Sustained Effect: {result.sustained_effect ? "Yes" : "No"}</p>
              <p>Side Effects Risk: {result.side_effects_risk}%</p>
              <p>Ranking Score: {result.ranking_score}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </motion.div>
  )
}

