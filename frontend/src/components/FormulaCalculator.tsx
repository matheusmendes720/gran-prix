import React, { useState } from 'react';
import { Card } from '../ui/card';
import { getFormulaById, FormulaTabConfig } from '../data/demoSnapshot';

interface FormulaCalculatorProps {
  formulaId: string;
}

export default function FormulaCalculator({ formulaId }: FormulaCalculatorProps) {
  const formula = getFormulaById(formulaId);
  const [inputs, setInputs] = useState(formula?.defaultInputs || {});
  const [selectedScenario, setSelectedScenario] = useState(0);
  
  if (!formula) return <div>Formula não encontrado</div>;
  
  const calculateResult = () => {
    try {
      // Simple eval for demo purposes - in production would use proper math parser
      const result = eval(formula.resultExpression.replace(/\b(\w+)\b/g, 'inputs.$1'));
      return {
        value: typeof result === 'number' ? Math.round(result * 100) / 100 : 0,
        unit: formulaId === 'pp' ? 'unidades' : formulaId === 'ss' ? 'unidades' : '%',
        narrative: `${formula.title}: ${result} unidades`,
        highlight: result > (formulaId === 'pp' ? 150 : formulaId === 'ss' ? 40 : 15) ? 'critical' : 
                 result > (formulaId === 'pp' ? 100 : formulaId === 'ss' ? 25 : 10) ? 'warning' : 'success'
      };
    } catch (e) {
      return { value: 0, unit: '', narrative: 'Erro no cálculo', highlight: 'critical' };
    }
  };
  
  const result = calculateResult();
  const scenario = formula.scenarios[selectedScenario];
  
  return (
    <Card className="p-6">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-2">{formula.title}</h2>
        <div className="bg-gray-50 p-3 rounded-lg mb-4">
          <div className="text-sm text-gray-600 font-mono text-center">
            {formula.latex}
          </div>
          <div className="text-xs text-gray-500 mt-1 text-center">
            {formula.summary}
          </div>
        </div>
      </div>
      
      {/* Input Fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {formula.inputs.map((input) => (
          <div key={input.id} className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {input.label}
            </label>
            {input.type === 'select' ? (
              <select
                value={inputs[input.id] || input.value}
                onChange={(e) => setInputs({...inputs, [input.id]: parseFloat(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                {input.options?.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type={input.type}
                value={inputs[input.id] || input.value}
                onChange={(e) => setInputs({...inputs, [input.id]: parseFloat(e.target.value)})}
                min={input.min}
                max={input.max}
                step={input.step}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            )}
            {input.min !== undefined && (
              <div className="text-xs text-gray-500">
                Range: {input.min} - {input.max}
              </div>
            )}
          </div>
        ))}
      </div>
      
      {/* Result Card */}
      <div className={`p-4 rounded-lg border-2 mb-6 ${
        result.highlight === 'critical' ? 'border-red-300 bg-red-50' :
        result.highlight === 'warning' ? 'border-yellow-300 bg-yellow-50' :
        'border-green-300 bg-green-50'
      }`}>
        <div className="flex justify-between items-start">
          <div>
            <div className="text-sm text-gray-600">Resultado</div>
            <div className="text-3xl font-bold text-gray-900">
              {result.value} {result.unit}
            </div>
            <div className={`text-sm font-medium mt-1 ${
              result.highlight === 'critical' ? 'text-red-600' :
              result.highlight === 'warning' ? 'text-yellow-600' :
              'text-green-600'
            }`}>
              {result.highlight === 'critical' ? '🔴 CRÍTICO' :
               result.highlight === 'warning' ? '🟡 ATENÇÃO' : '✅ OK'}
            </div>
          </div>
          <div className="text-sm text-gray-700 max-w-xs">
            {result.narrative}
          </div>
        </div>
      </div>
      
      {/* Scenario Cards */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Cenários</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {formula.scenarios.map((scenario, index) => (
            <div
              key={index}
              onClick={() => setSelectedScenario(index)}
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                selectedScenario === index
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300 bg-white'
              }`}
            >
              <div className="font-medium text-gray-900 mb-2">
                {scenario.name}
              </div>
              <div className="text-2xl font-bold text-blue-600 mb-1">
                {scenario.output} {result.unit}
              </div>
              <div className="text-sm text-gray-600">
                {scenario.narrative}
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Actions */}
      <div className="flex gap-3">
        {formula.actions.map((action) => (
          <button
            key={action.label}
            className="px-4 py-2 bg-blue-600 text-white rounded font-medium hover:bg-blue-700"
          >
            {action.label}
          </button>
        ))}
      </div>
    </Card>
  );
}