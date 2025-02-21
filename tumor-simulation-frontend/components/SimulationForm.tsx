"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface SimulationFormProps {
  onSubmit: (data: any) => void
  isLoading: boolean
}

export default function SimulationForm({ onSubmit, isLoading }: SimulationFormProps) {
  const [patientData, setPatientData] = useState({
    tumor_size: 100,
    tumor_carrying_capacity: 1000,
    tumor_growth_rate: 0.05,
    body_weight: 70,
    drug_types: ["Chemotherapy"],
    drug_doses: [100],
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setPatientData((prev) => ({ ...prev, [name]: Number.parseFloat(value) }))
  }

  const handleDrugTypeChange = (value: string, index: number) => {
    const newDrugTypes = [...patientData.drug_types]
    newDrugTypes[index] = value
    setPatientData((prev) => ({ ...prev, drug_types: newDrugTypes }))
  }

  const handleDrugDoseChange = (e: React.ChangeEvent<HTMLInputElement>, index: number) => {
    const newDrugDoses = [...patientData.drug_doses]
    newDrugDoses[index] = Number.parseFloat(e.target.value)
    setPatientData((prev) => ({ ...prev, drug_doses: newDrugDoses }))
  }

  const addDrug = () => {
    setPatientData((prev) => ({
      ...prev,
      drug_types: [...prev.drug_types, "Chemotherapy"],
      drug_doses: [...prev.drug_doses, 100],
    }))
  }

  const removeDrug = (index: number) => {
    setPatientData((prev) => ({
      ...prev,
      drug_types: prev.drug_types.filter((_, i) => i !== index),
      drug_doses: prev.drug_doses.filter((_, i) => i !== index),
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(patientData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <Label htmlFor="tumor_size">Initial Tumor Size (mm³)</Label>
          <Input
            id="tumor_size"
            name="tumor_size"
            type="number"
            value={patientData.tumor_size}
            onChange={handleInputChange}
            required
          />
        </div>
        <div>
          <Label htmlFor="tumor_carrying_capacity">Tumor Carrying Capacity (mm³)</Label>
          <Input
            id="tumor_carrying_capacity"
            name="tumor_carrying_capacity"
            type="number"
            value={patientData.tumor_carrying_capacity}
            onChange={handleInputChange}
            required
          />
        </div>
        <div>
          <Label htmlFor="tumor_growth_rate">Tumor Growth Rate</Label>
          <Input
            id="tumor_growth_rate"
            name="tumor_growth_rate"
            type="number"
            step="0.01"
            value={patientData.tumor_growth_rate}
            onChange={handleInputChange}
            required
          />
        </div>
        <div>
          <Label htmlFor="body_weight">Body Weight (kg)</Label>
          <Input
            id="body_weight"
            name="body_weight"
            type="number"
            value={patientData.body_weight}
            onChange={handleInputChange}
            required
          />
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Drug Treatments</h3>
        {patientData.drug_types.map((drugType, index) => (
          <div key={index} className="flex items-center space-x-4">
            <Select value={drugType} onValueChange={(value) => handleDrugTypeChange(value, index)}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Select drug type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Chemotherapy">Chemotherapy</SelectItem>
                <SelectItem value="Immunotherapy">Immunotherapy</SelectItem>
                <SelectItem value="Targeted Therapy">Targeted Therapy</SelectItem>
              </SelectContent>
            </Select>
            <Input
              type="number"
              value={patientData.drug_doses[index]}
              onChange={(e) => handleDrugDoseChange(e, index)}
              placeholder="Dose (mg)"
              className="w-32"
            />
            <Button type="button" variant="destructive" onClick={() => removeDrug(index)}>
              Remove
            </Button>
          </div>
        ))}
        <Button type="button" onClick={addDrug}>
          Add Drug
        </Button>
      </div>

      <Button type="submit" disabled={isLoading}>
        {isLoading ? "Simulating..." : "Run Simulation"}
      </Button>
    </form>
  )
}

