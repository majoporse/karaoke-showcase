{{/*
Expand the name of the chart.
*/}}
{{- define "karaoke-inator.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "karaoke-inator.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "karaoke-inator.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "karaoke-inator.labels" -}}
helm.sh/chart: {{ include "karaoke-inator.chart" . }}
{{ include "karaoke-inator.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "karaoke-inator.selectorLabels" -}}
app.kubernetes.io/name: {{ include "karaoke-inator.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Service labels for individual services
*/}}
{{- define "karaoke-inator.serviceLabels" -}}
{{- include "karaoke-inator.labels" . }}
app: {{ .serviceName }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "karaoke-inator.serviceAccountName" -}}
karaoke
{{- end }}

{{/*
Return the namespace for application
*/}}
{{- define "karaoke-inator.namespace" -}}
{{- .Values.global.namespace }}
{{- end }}

{{/*
Database connection string for orchestrator and other services
*/}}
{{- define "karaoke-inator.postgresql.host" -}}
{{ .Release.Name }}-postgresql
{{- end }}

{{/*
Redis URL for orchestrator and RQ worker
*/}}
{{- define "karaoke-inator.redis.url" -}}
redis://{{ .Release.Name }}-redis-master:6379/0
{{- end }}

{{/*
MinIO endpoint for orchestrator and services
Uses standard MinIO Deployment in the same namespace
*/}}
{{- define "karaoke-inator.minio.endpoint" -}}
minio.{{ .Release.Namespace }}.svc.cluster.local:9000
{{- end }}

{{/*
Service discovery URLs for orchestrator
*/}}
{{- define "karaoke-inator.voiceSeparation.url" -}}
http://voice-separation:{{ .Values.voiceSeparation.port }}
{{- end }}

{{- define "karaoke-inator.lyricsExtraction.url" -}}
http://lyrics-extraction:{{ .Values.lyricsExtraction.port }}
{{- end }}

{{- define "karaoke-inator.songManagement.url" -}}
http://song-management:{{ .Values.songManagement.port }}
{{- end }}

{{/*
OTEL Collector endpoint
*/}}
{{- define "karaoke-inator.otel.endpoint" -}}
{{ .Release.Name }}-otel-collector:4317
{{- end }}

{{/*
PostgreSQL fullname
*/}}
{{- define "karaoke-inator.postgresql.fullname" -}}
{{ include "karaoke-inator.fullname" . }}-postgresql
{{- end }}

{{/*
Secrets fullname
*/}}
{{- define "karaoke-inator.secrets.fullname" -}}
{{ include "karaoke-inator.fullname" . }}-secrets
{{- end }}

{{/*
Generate a random password if not provided (only for secrets)
*/}}
{{- define "karaoke-inator.randomPassword" -}}
{{- randAlphaNum 32 }}
{{- end }}

{{/*
Generate Docker config JSON for registry authentication
*/}}
{{- define "karaoke-inator.dockerconfigjson" -}}
{{- $auth := printf "%s:%s" .Values.image.auth.username .Values.image.auth.password | b64enc -}}
{
  "auths": {
    "{{ .Values.image.registry }}": {
      "auth": "{{ $auth }}"
    }
  }
}
{{- end }}
