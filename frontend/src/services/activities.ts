import { apiRequest } from './api'
import type {ActivityRule} from '../types/activity'

export async function getActivities(): Promise<ActivityRule[]> {
    const response = await apiRequest('/activities')
    return response.json()
}