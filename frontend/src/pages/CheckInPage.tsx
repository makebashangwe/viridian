import { useEffect, useState } from 'react'
import { getActivities } from '../services/activities'
import type { ActivityRule } from '../types/activity'

function CheckInPage(){
    const [activities, setActivities] = useState<ActivityRule[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState('')
    const [selectedActivityId, setSelectedActivityId] = useState('')
    const [durationMinutes, setDurationMinutes] = useState('')

    useEffect(() => {
    async function loadActivities() {
        try{
            const activityData = await getActivities()
            setActivities(activityData)
        } catch {
            setError('We could not load your activities.')
        }finally{
            setIsLoading(false)
        }
    }

    void loadActivities()
    }, [])
    if (isLoading) {
        return <p role="status">Loading activities…</p>
    }

    if (error) {
        return <p role="alert">{error}</p>
    }

    return(
        <section>
            <h1>Check In</h1>
            <p>Let us know what you did today.</p>
                <label htmlFor="activity">Activity</label>

                <select
                id="activity"
                value={selectedActivityId}
                onChange={(event) => setSelectedActivityId(event.target.value)}
                required
                >
                <option value="">Choose an activity</option>

                {activities.map((activity) => (
                    <option key={activity.id} value={activity.id}>
                    {activity.name}
                    </option>
                ))}
                </select>

                <label htmlFor="duration">Duration in minutes</label>

                    <input
                    id="duration"
                    type="number"
                    min="1"
                    value={durationMinutes}
                    onChange={(event) => setDurationMinutes(event.target.value)}
                    required
                    />
        </section>
    );
}
export default CheckInPage

