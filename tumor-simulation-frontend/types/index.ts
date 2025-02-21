export interface SimulationResult {
  drug: string
  dose: number
  final_tumor_size: number
  tumor_reduction_percent: number
  time_to_half_size: number | null
  ranking_score: number
  sustained_effect: boolean
  side_effects_risk: number
}

