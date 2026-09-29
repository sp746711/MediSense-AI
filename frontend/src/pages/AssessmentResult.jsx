import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import AssessmentStatus from '../components/AssessmentStatus';
import EvidenceCard from '../components/EvidenceCard';
import ErrorMessage from '../components/ErrorMessage';
import LoadingScreen from '../components/LoadingScreen';
import { getAssessment, getAssessmentResult } from '../services/assessmentService';
import { formatDate, inputTypesLabel } from '../utils/formatters';
import { MEDICAL_DISCLAIMER } from '../utils/constants';

export default function AssessmentResult() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [assessment, setAssessment] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const [a, r] = await Promise.all([getAssessment(id), getAssessmentResult(id)]);
        if (!active) return;
        setAssessment(a);
        setResult(r);
      } catch (err) {
        if (active) setError(err.message);
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, [id]);

  if (loading) return <LoadingScreen message="Loading assessment..." />;

  const pathway = result?.pathway || assessment?.pathway;
  const upper = String(pathway || '').toUpperCase();

  return (
    <div className="page">
      <h1>Final Health Outcome</h1>
      <ErrorMessage message={error} onDismiss={() => setError('')} />

      <p>
        <strong>Assessment Date:</strong> {formatDate(assessment?.created_at)}
      </p>
      <p>
        <strong>Inputs:</strong> {inputTypesLabel(assessment?.input_types)}
      </p>

      <AssessmentStatus pathway={pathway} status={result?.status || assessment?.status} />

      {!pathway ? (
        <p className="info-banner">
          {result?.message ||
            'Available information is insufficient for a specific conclusion, or processing is not complete yet.'}
        </p>
      ) : null}

      <div className="evidence-grid">
        <EvidenceCard title="SYMPTOMS" emptyText="No structured symptom evidence yet." />
        <EvidenceCard title="MEDICAL REPORT" emptyText="No extracted report findings yet." />
        <EvidenceCard title="X-RAY ANALYSIS" emptyText="No X-ray model result yet, or interpretation unavailable." />
        <EvidenceCard title="WHY THIS PATHWAY?">
          <p>
            Pathway is selected by the backend safety/rules engine — not independently by the LLM.
            {pathway ? ` Current pathway: ${pathway}.` : ' Pathway not determined.'}
          </p>
        </EvidenceCard>
        <EvidenceCard title="UNCERTAINTY / LIMITATIONS">
          <p>
            Insufficient or pending multimodal processing may limit conclusions. Model confidence is not a clinical probability.
          </p>
        </EvidenceCard>
        <EvidenceCard title="SUGGESTED SPECIALTY">
          <p>{assessment?.specialty || 'Insufficient evidence for a suggested specialty.'}</p>
        </EvidenceCard>
        <EvidenceCard title="GENERAL GUIDANCE">
          <p>This system does not prescribe medicines or provide definitive diagnosis.</p>
        </EvidenceCard>
        <EvidenceCard title="RECOMMENDED NEXT STEPS">
          <p>Use the pathway-specific actions below. Seek emergency care for urgent symptoms.</p>
        </EvidenceCard>
      </div>

      <div className="action-row">
        {upper === 'EMERGENCY' ? (
          <>
            <button type="button" className="btn btn-primary" onClick={() => navigate('/facilities')}>
              Find Emergency Facilities
            </button>
            <button type="button" className="btn btn-secondary" onClick={() => navigate('/assistant')}>
              Ask AI Assistant
            </button>
          </>
        ) : null}
        {upper === 'CONSULTATION' ? (
          <>
            <button type="button" className="btn btn-primary" onClick={() => navigate('/doctors')}>
              Find Doctors
            </button>
            <button type="button" className="btn btn-secondary" onClick={() => navigate('/facilities')}>
              Find Facilities
            </button>
            <button type="button" className="btn btn-secondary" onClick={() => navigate('/assistant')}>
              Ask AI Assistant
            </button>
          </>
        ) : null}
        {upper === 'MILD' ? (
          <>
            <button type="button" className="btn btn-primary" onClick={() => navigate(`/assessment/${id}/details`)}>
              General Guidance
            </button>
            <button type="button" className="btn btn-secondary" onClick={() => navigate('/medical-shops')}>
              Find Medical Shops
            </button>
            <button type="button" className="btn btn-secondary" onClick={() => navigate('/assistant')}>
              Ask AI Assistant
            </button>
          </>
        ) : null}
        {!upper || !['EMERGENCY', 'CONSULTATION', 'MILD'].includes(upper) ? (
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/assistant')}>
            Ask AI Assistant
          </button>
        ) : null}
        <button type="button" className="btn btn-secondary" onClick={() => navigate(`/assessment/${id}/details`)}>
          View Details
        </button>
        <button type="button" className="btn btn-secondary" onClick={() => setError('PDF download will be available after full assessment processing.')}>
          Download Assessment Report
        </button>
        <button type="button" className="btn btn-secondary" onClick={() => navigate('/dashboard')}>
          Back to Dashboard
        </button>
      </div>

      <p className="disclaimer-inline">{MEDICAL_DISCLAIMER}</p>
    </div>
  );
}
