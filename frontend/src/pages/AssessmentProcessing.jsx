import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoadingScreen from '../components/LoadingScreen';
import ErrorMessage from '../components/ErrorMessage';
import { processAssessment } from '../services/assessmentService';
import { useAssessment } from '../hooks/useAssessment';

const STEPS = [
  'Validating input',
  'Processing symptoms',
  'Processing medical report',
  'Analyzing X-ray',
  'Checking evidence',
  'Applying safety rules',
  'Preparing assessment',
];

export default function AssessmentProcessing() {
  const navigate = useNavigate();
  const { assessmentId } = useAssessment();
  const [step, setStep] = useState(0);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!assessmentId) {
      setError('No assessment in progress.');
      return undefined;
    }

    let cancelled = false;
    let timer;

    const run = async () => {
      try {
        for (let i = 0; i < STEPS.length; i += 1) {
          if (cancelled) return;
          setStep(i);
          await new Promise((r) => {
            timer = setTimeout(r, 450);
          });
        }
        const result = await processAssessment(assessmentId);
        if (cancelled) return;
        setMessage(result.message || 'Processing accepted.');
        navigate(`/assessment/${assessmentId}`, { replace: true });
      } catch (err) {
        if (!cancelled) setError(err.message);
      }
    };

    run();
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [assessmentId, navigate]);

  if (error) {
    return (
      <div className="page narrow">
        <ErrorMessage message={error} />
        <button type="button" className="btn btn-secondary" onClick={() => navigate('/dashboard')}>
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="page narrow">
      <LoadingScreen message={STEPS[step] || 'Processing...'} />
      <ul className="process-steps">
        {STEPS.map((label, idx) => (
          <li key={label} className={idx <= step ? 'active' : ''}>
            {label}
          </li>
        ))}
      </ul>
      {message ? <p className="muted">{message}</p> : null}
    </div>
  );
}
