import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ErrorMessage from '../components/ErrorMessage';
import { submitSymptoms } from '../services/symptomService';
import { useAssessment } from '../hooks/useAssessment';
import { INPUT_TYPES } from '../utils/constants';

export default function SymptomsInput() {
  const navigate = useNavigate();
  const { assessmentId, inputTypes } = useAssessment();
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const nextPath = () => {
    if (inputTypes.includes(INPUT_TYPES.MEDICAL_REPORT)) return '/assessment/report';
    if (inputTypes.includes(INPUT_TYPES.XRAY)) return '/assessment/xray';
    return '/assessment/processing';
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!assessmentId) return setError('No assessment in progress. Start a new assessment.');
    if (!text.trim()) return setError('Please describe your symptoms.');
    setSubmitting(true);
    try {
      await submitSymptoms(assessmentId, text.trim());
      navigate(nextPath());
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page narrow">
      <h1>Symptoms</h1>
      <p className="muted">
        Describe symptoms naturally. Example: &quot;I have cough and fever for 3 days. I don&apos;t have chest pain.&quot;
      </p>
      <ErrorMessage message={error} onDismiss={() => setError('')} />
      <form onSubmit={onSubmit} className="stack-form">
        <label>
          Symptom description
          <textarea
            rows={8}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Describe what you are experiencing..."
            required
          />
        </label>
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? 'Saving...' : 'Continue'}
        </button>
      </form>
    </div>
  );
}
